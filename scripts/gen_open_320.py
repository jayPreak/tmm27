import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json, datetime as dt
E=(330,360); MP=(280,288); T=(265,272); I=(245,252); EP=345
def p(s): return f"{s//60}:{s%60:02d}"
def pr(r): return f"{p(r[0])}-{p(r[1])}/km"
HE="65-78% of max HR"; HM="80-85% of max HR"; HT="86-90% of max HR"; HI="92-95% of max HR"
def wo(id,name,km,mins,zone,hr,desc,typ,sport="run"):
    return {"id":id,"sport":sport,"type":typ,"name":name,"description":desc,"durationMinutes":round(mins),
            "distanceMeters":int(round(km*1000)) if km else None,"primaryZone":zone,"humanReadable":hr,"completed":False}
def easy(id,km,strides=False,rec=False):
    h=f"{km} km easy @ {pr(E)} ({HE}). Conversational the whole way."
    if strides: h+="\nThen 6x20 s strides, fast and relaxed, 40 s walk between"
    return wo(id,("Recovery " if rec else "Easy ")+f"{km}k"+(" + strides" if strides else ""),km,km*EP/60+(3 if strides else 0),"Zone 2",h,"Aerobic volume.","recovery" if rec else "endurance")
def long(id,km,mp_km=0,note=""):
    mins=(km-mp_km)*EP/60+mp_km*284/60
    h=f"{km} km. "+(f"Easy @ {pr(E)} for {km-mp_km-2} km, then {mp_km} km @ marathon pace {pr(MP)}, then 2 km easy" if mp_km else f"Steady easy @ {pr(E)} ({HE})")
    if km>=20: h+="\nFuel: 30-40 g carbs every 30 min from 40 min in, plus 400-700 ml fluid per hour with electrolytes"
    if note: h+="\n"+note
    return wo(id,f"Long run {km}k"+(f" with {mp_km}k at MP" if mp_km else ""),km,mins,"Zone 2"+(" + MP" if mp_km else ""),h,"Key session.","long")
def q(id,name,km,mins,zone,h,typ): return wo(id,name,km,mins,zone,h,"Key session. Warm-up and cool-down are easy running.",typ)
def thr(id,reps,mn,rec):
    km=round(5+reps*mn*60/268,1); mins=5*EP/60+reps*mn+(reps-1)*rec/60
    return q(id,f"Threshold {reps}x{mn} min",km,mins,"Threshold",f"2.5 km easy warm-up + 4 strides\n{reps}x{mn} min @ {pr(T)} ({HT}), {rec} s easy jog between\n2.5 km easy cool-down","threshold")
def ints(id,reps,m,rec):
    km=round(5+reps*m/1000+reps*0.3,1); mins=5*EP/60+reps*m/1000*248/60+reps*rec/60
    return q(id,f"Intervals {reps}x{m} m",km,mins,"VO2max",f"2.5 km easy warm-up + 4 strides\n{reps}x{m} m @ {pr(I)} ({HI}), {rec//60} min easy jog between\n2.5 km easy cool-down","vo2max")
def mp(id,k,blocks=1):
    km=4+k+(blocks-1); mins=4*EP/60+k*284/60+(blocks-1)*330/60
    b=f"{k} km" if blocks==1 else f"{blocks}x{k//blocks} km with 1 km easy between"
    return q(id,f"Marathon pace {k}k",km,mins,"Marathon pace",f"2 km easy warm-up\n{b} @ {pr(MP)} ({HM}). Smooth and controlled; practise drinking on the move\n2 km easy cool-down","tempo")
def hm(id):
    return q(id,"Half marathon tune-up",21.1+3,21.1*275/60+3*EP/60,"Race",f"1.5 km easy warm-up + strides\n21.1 km race or solo time trial, even effort. Target 1:35-1:37 (4:30-4:35/km)\n1.5 km easy cool-down. Under 1:35 supports 3:20; slower than 1:38 means race at 3:25-3:30","test")
def rest(id,txt="Rest day. Optional 30-40 min easy cross-training (bike, swim) at conversational effort."):
    return {"id":id,"sport":"rest","type":"rest","name":"Rest","description":txt,"completed":False}
W={}
def wk(n,ph,focus,rec,d): W[n]=(ph,focus,rec,d)
X="o320"
def W4(n,ph,focus,rec,d):
    d.setdefault(0,rest(f"{X}-w{n}-mon","Rest. Optional strength or 30-40 min easy cross-training."))
    d.setdefault(3,rest(f"{X}-w{n}-thu","Rest. Optional 30-40 min easy cross-training (bike, swim)."))
    d.setdefault(5,rest(f"{X}-w{n}-sat","Rest before the long run. Optional mobility or light strength."))
    wk(n,ph,focus,rec,d)
W4(1,"Base","Settle into four runs a week",False,{1:thr(f"{X}-w1-tue",3,8,90),2:easy(f"{X}-w1-wed",10),4:mp(f"{X}-w1-fri",6),6:long(f"{X}-w1-sun",20)})
W4(2,"Base","Aerobic volume, first VO2 session",False,{1:ints(f"{X}-w2-tue",6,800,120),2:easy(f"{X}-w2-wed",11,True),4:mp(f"{X}-w2-fri",8),6:long(f"{X}-w2-sun",22)})
W4(3,"Base","Longer threshold, steady long run",False,{1:thr(f"{X}-w3-tue",3,10,90),2:easy(f"{X}-w3-wed",12),4:mp(f"{X}-w3-fri",10),6:long(f"{X}-w3-sun",24)})
W4(4,"Base","Easier week. Volume down about a quarter",True,{1:thr(f"{X}-w4-tue",2,10,90),2:easy(f"{X}-w4-wed",9),4:easy(f"{X}-w4-fri",9,True),6:long(f"{X}-w4-sun",18)})
W4(5,"Build","Marathon-specific work begins",False,{1:ints(f"{X}-w5-tue",5,1000,120),2:easy(f"{X}-w5-wed",12,True),4:mp(f"{X}-w5-fri",12),6:long(f"{X}-w5-sun",26,6)})
W4(6,"Build","Threshold volume up",False,{1:thr(f"{X}-w6-tue",4,10,90),2:easy(f"{X}-w6-wed",13),4:mp(f"{X}-w6-fri",14,2),6:long(f"{X}-w6-sun",28)})
W4(7,"Build","Biggest build week",False,{1:ints(f"{X}-w7-tue",6,1000,120),2:easy(f"{X}-w7-wed",13,True),4:mp(f"{X}-w7-fri",14),6:long(f"{X}-w7-sun",30,10)})
W4(8,"Build","Easier week with a half marathon tune-up",True,{1:thr(f"{X}-w8-tue",2,12,90),2:easy(f"{X}-w8-wed",8),4:easy(f"{X}-w8-fri",6,True),5:rest(f"{X}-w8-sat","Rest before Sunday's half marathon."),6:hm(f"{X}-w8-sun")})
W4(9,"Peak","Peak volume",False,{1:thr(f"{X}-w9-tue",3,15,120),2:easy(f"{X}-w9-wed",14),4:mp(f"{X}-w9-fri",16,2),6:long(f"{X}-w9-sun",32,8)})
W4(10,"Peak","Last big week. 34 km race rehearsal",False,{1:ints(f"{X}-w10-tue",5,1200,120),2:easy(f"{X}-w10-wed",13,True),4:mp(f"{X}-w10-fri",12),6:long(f"{X}-w10-sun",34,16,"Structure: 15 km easy, 2x8 km at MP with 1 km easy between, 2 km easy. Race-day breakfast, kit and fuel.")})
W4(11,"Taper","Volume down about 30%, intensity stays",False,{1:thr(f"{X}-w11-tue",3,8,90),2:easy(f"{X}-w11-wed",10),4:mp(f"{X}-w11-fri",10),6:long(f"{X}-w11-sun",21,8)})
W4(12,"Taper","Race week",False,{1:q(f"{X}-w12-tue","Marathon pace sharpener",10,10*300/60,"Marathon pace",f"2 km easy warm-up\n3x2 km @ {pr(MP)}, 2 min jog between\n2 km easy cool-down","tempo"),2:easy(f"{X}-w12-wed",7),4:easy(f"{X}-w12-fri",6,True),
 3:rest(f"{X}-w12-thu","Rest. Carb load Friday and Saturday: 8-10 g carbs per kg body weight per day."),5:rest(f"{X}-w12-sat","Rest. Lay out kit, sleep early."),
 6:{"id":f"{X}-w12-race","sport":"run","type":"race","name":"TATA MUMBAI MARATHON","description":"Race day.","durationMinutes":200,"distanceMeters":42195,"primaryZone":"Marathon pace","humanReadable":"Goal 3:20 (4:44/km). Km 0-5 at 4:48-4:50. Km 5-30 at 4:42-4:46. Km 30 on: hold, push only if controlled. Gel every 30 min.","completed":False}})

DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
start=dt.date(2026,10,26); weeks=[]
for n in range(1,13):
    ph,focus,rec,d=W[n]; ws=start+dt.timedelta(weeks=n-1); dl=[]; km=h=s=0
    for i in range(7):
        w=d.get(i, rest(f"{X}-w{n}-{i}")); 
        if w["sport"]=="run": km+=w["distanceMeters"]/1000; h+=w["durationMinutes"]/60; s+=1
        dl.append({"date":(ws+dt.timedelta(days=i)).isoformat(),"dayOfWeek":DAYS[i],"workouts":[w]})
    weeks.append({"weekNumber":n,"startDate":ws.isoformat(),"endDate":(ws+dt.timedelta(days=6)).isoformat(),"phase":ph,"focus":focus,
      "targetHours":round(h,1),"isRecoveryWeek":rec,"days":dl,"summary":{"totalHours":round(h,1),"bySport":{"run":{"sessions":s,"hours":round(h,1),"km":round(km,1)}}}})
plan={"version":"1.0","meta":{"id":"tmm-2027-open-320","athlete":"Anyone","event":"Tata Mumbai Marathon 2027","eventDate":"2027-01-17","planStartDate":"2026-10-26","planEndDate":"2027-01-17","totalWeeks":12,"generatedBy":"Claude Coach (coros-coach)"},
 "phases":[{"name":"Base","startWeek":1,"endWeek":4,"focus":"Aerobic volume and threshold"},{"name":"Build","startWeek":5,"endWeek":8,"focus":"Marathon pace volume"},{"name":"Peak","startWeek":9,"endWeek":10,"focus":"Highest volume and race rehearsal"},{"name":"Taper","startWeek":11,"endWeek":12,"focus":"Shed fatigue"}],
 "weeks":weeks}
json.dump(plan,open(os.path.join(ROOT, "plans/open-320.json"),"w"),indent=1,ensure_ascii=False)
print([w["summary"]["bySport"]["run"]["km"] for w in weeks])
