#!/usr/bin/env python3
"""Conservative Deluge cleanup for long-inactive incomplete torrents.

DRY RUN by default. Pass --live to allow removal.
Uses Deluge Web JSON-RPC; standard library only.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

URL=os.environ.get("DELUGE_URL","http://127.0.0.1:8112").rstrip("/")
PASSWORD=os.environ.get("DELUGE_PASSWORD","")
INACTIVE_DAYS=float(os.environ.get("DELUGE_INACTIVE_DAYS","11"))
ACTIVITY_BPS=float(os.environ.get("DELUGE_ACTIVITY_BPS","1024"))
REMOVE_DATA=os.environ.get("DELUGE_REMOVE_DATA","true").lower() in ("1","true","yes","on")
STATE=os.environ.get("DELUGE_CLEANUP_STATE",os.path.join(os.path.dirname(os.path.abspath(__file__)),"deluge-smart-cleanup-state.json"))
COOKIE=None
RPC_ID=0

def rpc(method, params=None):
    global RPC_ID, COOKIE
    RPC_ID += 1
    data=json.dumps({"method":method,"params":params or [],"id":RPC_ID}).encode()
    headers={"Content-Type":"application/json"}
    if COOKIE: headers["Cookie"]=COOKIE
    req=urllib.request.Request(URL+"/json",data=data,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        sc=r.headers.get("Set-Cookie")
        if sc: COOKIE=sc.split(";",1)[0]
        obj=json.load(r)
    if obj.get("error"): raise RuntimeError(str(obj["error"]))
    return obj.get("result")

def load_state():
    try:
        with open(STATE,"r",encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError): return {"torrents":{}}

def save_state(s):
    tmp=STATE+".tmp"
    os.makedirs(os.path.dirname(STATE) or ".",exist_ok=True)
    with open(tmp,"w",encoding="utf-8") as f: json.dump(s,f,indent=2,sort_keys=True)
    os.replace(tmp,STATE)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--live",action="store_true",help="actually remove qualifying torrents")
    args=ap.parse_args()
    if not PASSWORD:
        sys.exit("ERROR: DELUGE_PASSWORD is required")
    rpc("auth.login",[PASSWORD])
    fields=["name","progress","state","download_payload_rate","upload_payload_rate","total_done"]
    torrents=rpc("web.update_ui",[fields,{}])["torrents"]
    st=load_state(); now=time.time(); seen=set()
    for tid,t in torrents.items():
        seen.add(tid)
        progress=float(t.get("progress") or 0)
        down=float(t.get("download_payload_rate") or 0)
        up=float(t.get("upload_payload_rate") or 0)
        done=int(t.get("total_done") or 0)
        name=t.get("name") or tid
        e=st["torrents"].setdefault(tid,{"last_active":now,"last_done":done})
        active=(down>=ACTIVITY_BPS or up>=ACTIVITY_BPS or done>int(e.get("last_done",0)))
        if active:
            e["last_active"]=now
        e["last_done"]=done
        if progress >= 100.0:
            # Completed torrents belong to the seeding-retention policy.
            st["torrents"].pop(tid,None)
            continue
        inactive_days=(now-float(e.get("last_active",now)))/86400.0
        if inactive_days < INACTIVE_DAYS:
            print(f"KEEP  {name}: {progress:.1f}% inactive {inactive_days:.1f}/{INACTIVE_DAYS:g} days")
            continue
        print(f"{'REMOVE' if args.live else 'WOULD REMOVE'}  {name}: {progress:.1f}% inactive {inactive_days:.1f} days")
        if args.live:
            ok=rpc("core.remove_torrent",[tid,REMOVE_DATA])
            if ok is False:
                print("  WARNING: Deluge reported removal failure",file=sys.stderr)
            else:
                st["torrents"].pop(tid,None)
    for tid in list(st["torrents"]):
        if tid not in seen: st["torrents"].pop(tid,None)
    save_state(st)
    print("LIVE mode" if args.live else "DRY RUN - nothing was removed")

if __name__=="__main__":
    try: main()
    except (urllib.error.URLError,RuntimeError,KeyError) as e:
        sys.exit("ERROR: "+str(e))
