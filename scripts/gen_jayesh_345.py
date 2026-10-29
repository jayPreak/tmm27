import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json, datetime as dt
D=dt.date
E=(370,400)      # easy pace s/km
MP=(318,326)     # goal MP 5:18-5:26
T=(305,315); I=(285,295)
def p(s): return f"{s//60}:{s%60:02d}"
def pr(r): return f"{p(r[0])}-{p(r[1])}/km"
HR_E="134-147 bpm"; HR_MP="150-158 bpm"; HR_T="158-166 bpm"; HR_I="167-174 bpm"

def wo(id,name,km,mins,zone,hr,desc,typ="endurance",sport="run",done=False):
    return {"id":id,"sport":sport,"type":typ,"name":name,"description":desc,"durationMinutes":round(mins),
            "distanceMeters":int(km*1000) if km else None,"primaryZone":zone,"humanReadable":hr,"completed":done}

def easy(id,km,strides=False):
    mins=km*385/60+(3 if strides else 0)
    h=f"{km} km easy @ {pr(E)}, HR {HR_E} (cap 147 — slow down in heat, pace is secondary)"
    if strides: h+="\nThen 6x20s strides (fast, relaxed, ~4:30/km) w/ 40s walk"
    return wo(id,f"Easy {km}k"+(" + strides" if strides else ""),km,mins,"Zone 2",h,"Aerobic volume. Conversational.","endurance" if not strides else "endurance")
def long(id,km,mp_km=0,note=""):
    e_km=km-mp_km
    mins=e_km*385/60+mp_km*322/60
    h=f"{km} km total. "
    if mp_km: h+=f"First {e_km-2 if mp_km else e_km} km easy @ {pr(E)} (HR ≤147) → {mp_km} km @ MP {pr(MP)} (HR {HR_MP}) → 2 km easy"
    else: h+=f"Steady easy @ {pr(E)}, HR {HR_E}"
    if km>=18: h+="\nFuel: gel/~30g carbs every 30-35 min from 40 min in + 400-600 ml fluid/h w/ electrolytes (rehearse race-day fuel)"
    if note: h+="\n"+note
    return wo(id,f"Long run {km}k"+(f" w/ {mp_km}k MP" if mp_km else ""),km,mins,"Zone 2" if not mp_km else "Zone 2 + MP",h,
              "Key session. Builds endurance + fuelling practice.","long")
def q(id,name,km,mins,zone,h,typ="threshold"):
    return wo(id,name,km,mins,zone,h,"Key quality session. Full 2 km warm-up + 2 km cool-down easy.",typ)
def thr(id,reps,rep,rec):
    km=4+reps*rep*0+0
    work=reps*rep
    tot_km=round(4+work*1000/310/60*0+ (reps*rep*60/310)+ (reps-1)*rec/400,1)
    mins=4*385/60+reps*rep+(reps-1)*rec/60
    return q(id,f"Threshold {reps}x{rep}min",tot_km,mins,"Zone 4-5a",
      f"2 km easy WU + 4 strides\n{reps}x{rep} min @ T {pr(T)} (HR {HR_T}), {rec}s easy jog between\n2 km easy CD")
def thr_km(id,reps,dist,rec):
    km=round(4+reps*dist+(reps-1)*0.3,1)
    mins=4*385/60+reps*dist*310/60+(reps-1)*rec/60
    return q(id,f"Threshold {reps}x{dist}km",km,mins,"Zone 4-5a",
      f"2 km easy WU + 4 strides\n{reps}x{dist} km @ T {pr(T)} (HR {HR_T}), {rec}s easy jog between\n2 km easy CD")
def ints(id,reps,dist,rec):
    km=round(4+reps*dist+(reps)*0.3,1)
    mins=4*385/60+reps*dist*290/60+reps*rec/60
    return q(id,f"Intervals {reps}x{int(dist*1000)}m",km,mins,"Zone 5b",
      f"2 km easy WU + 4 strides\n{reps}x{int(dist*1000)} m @ {pr(I)} (HR {HR_I} by end of rep), {rec//60} min easy jog between\n2 km easy CD","vo2max")
def mp(id,mpkm,blocks=1,float_km=0):
    km=4+mpkm+float_km*(blocks-1)
    mins=4*385/60+mpkm*322/60+float_km*(blocks-1)*370/60
    b=f"{mpkm} km @ MP" if blocks==1 else f"{blocks}x{mpkm//blocks} km @ MP w/ {float_km} km easy float between"
    return q(id,f"Marathon pace {mpkm}k",km,mins,"MP (Z3)",
      f"2 km easy WU\n{b} — {pr(MP)}, HR {HR_MP}. Smooth, not forced; practise drinking on the move\n2 km easy CD","tempo")
def tt(id):
    return q(id,"30-min threshold test",9,70,"Test",
      "2 km easy WU + 4 strides\n30 min solo all-out-but-even (flat route, early AM)\nRecord: avg pace + avg HR of LAST 20 min = new LT pace / LTHR → I re-set MP\n2 km easy CD","test")
def rest(id,note="No running. Strength day (your programme)."):
    return {"id":id,"sport":"rest","type":"rest","name":"No run — strength","description":note,"completed":False}
def bike(id,mins=45):
    return wo(id,f"Optional easy spin {mins}min",None,mins,"Zone 1-2",
      f"{mins} min road/indoor bike, HR 115-135. Pure recovery flush after deadlifts — skip if legs are smashed.","Optional cross-training. Marathon is priority.","recovery","bike")

DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
start=D(2026,10,26)
# per week: {weekday_index: [workouts]}, phase, focus, recovery
W={}
def wk(n,phase,focus,rec,days): W[n]=(phase,focus,rec,days)
done=lambda w: {**w,"completed":True}
def R(n,i):
    return {0:rest(f"w{n}-mon","Press day (shoulders and arms). No run."),
            3:rest(f"w{n}-thu","Full rest. Optional 30-45 min easy spin, HR 115-135."),
            5:rest(f"w{n}-sat","Deadlift day. No run. Keep it at RPE 8 or below before the long run.")}[i]
def W4(n,phase,focus,rec,d):
    for i in (0,3,5):
        d.setdefault(i,[R(n,i)])
    wk(n,phase,focus,rec,d)
FRI="Run in the morning, squat later in the day."
W4(1,"Rebuild","Restart on four runs a week. HRV is a little below baseline, so keep it easy",False,{
 0:[rest("w1-mon","Done: strength.")],
 1:[done(wo("w1-tue","Done: 6.5k incl 1k reps",6.6,46,"mixed","Already completed (Oct 27).","endurance"))],
 2:[done(wo("w1-wed","Done: 6k easy",6.1,48,"Zone 2","Already completed (Oct 28).","endurance"))],
 4:[easy("w1-fri",6)],6:[long("w1-sun",14)]})
W4(2,"Rebuild","Four runs a week, first light quality",False,{
 1:[q("w2-tue","Fartlek 8x1min",7,45,"Zone 2 + 5b","2 km easy WU\n8x1 min brisk @ ~4:50/km / 1 min easy jog\n2 km easy CD","vo2max")],
 2:[easy("w2-wed",6)],4:[mp("w2-fri",3)],6:[long("w2-sun",16)]})
W4(3,"Base","First threshold session",False,{
 1:[thr("w3-tue",3,8,120)],2:[easy("w3-wed",7,True)],4:[mp("w3-fri",5)],6:[long("w3-sun",18)]})
W4(4,"Base","Easier week with a threshold test. Line up your strength deload",True,{
 1:[tt("w4-tue")],2:[easy("w4-wed",6)],4:[easy("w4-fri",6,True)],6:[long("w4-sun",13)]})
W4(5,"Build","Marathon-specific work begins",False,{
 1:[ints("w5-tue",5,1.0,120)],2:[easy("w5-wed",8)],4:[mp("w5-fri",6)],6:[long("w5-sun",21)]})
W4(6,"Build","Threshold and longer marathon pace",False,{
 1:[thr_km("w6-tue",4,1.6,90)],2:[easy("w6-wed",8,True)],4:[mp("w6-fri",8)],6:[long("w6-sun",24)]})
W4(7,"Build","First long run with a marathon pace finish",False,{
 1:[ints("w7-tue",6,1.0,120)],2:[easy("w7-wed",9)],4:[mp("w7-fri",8,2,1)],6:[long("w7-sun",26,6)]})
W4(8,"Build","Easier week with a retest that sets the goal (3:45 or 3:40)",True,{
 1:[tt("w8-tue")],2:[easy("w8-wed",7)],4:[easy("w8-fri",7,True)],6:[long("w8-sun",16,5)]})
W4(9,"Peak","Biggest volume",False,{
 1:[thr_km("w9-tue",3,3,120)],2:[easy("w9-wed",10)],4:[mp("w9-fri",10)],
 6:[long("w9-sun",29,5,"Progressive: last 5 km at MP. Full race kit and breakfast rehearsal (wake 3:30, run 5:15)")]})
W4(10,"Peak","Last big week. 32k race rehearsal",False,{
 1:[ints("w10-tue",5,1.2,120)],2:[easy("w10-wed",10,True)],4:[mp("w10-fri",8)],
 5:[rest("w10-sat","Deadlift day. Cap at RPE 7, long run tomorrow.")],
 6:[long("w10-sun",32,15,"Structure: 12 km easy, then 3x5 km at MP with 1 km easy between (count the floats as easy), then 3 km easy. Exact race fuel.")]})
W4(11,"Taper","Volume down about 30%, intensity stays. Light lower-body lifting",False,{
 1:[thr_km("w11-tue",3,2,120)],2:[easy("w11-wed",7)],4:[mp("w11-fri",8)],
 5:[rest("w11-sat","Pull day, light. No heavy deadlift.")],6:[long("w11-sun",18,6)]})
W4(12,"Race","Race week. No heavy lower-body lifting",False,{
 1:[q("w12-tue","MP sharpener 3x1.6k",9,52,"MP","2 km easy WU\n3x1.6 km @ MP 5:18-5:26/km, 2 min jog between\n2 km easy CD","tempo")],
 2:[easy("w12-wed",5)],
 3:[rest("w12-thu","Full rest. Carb loading starts Friday.")],
 4:[easy("w12-fri",5,True)],
 5:[rest("w12-sat","Rest. Carb load (8-10 g per kg). Bib pickup, kit laid out, sleep early. No deadlift.")],
 0:[rest("w12-mon","Upper body only, light.")],
 6:[{"id":"w12-sun-race","sport":"run","type":"race","name":"TATA MUMBAI MARATHON","description":"Race day.",
     "durationMinutes":225,"distanceMeters":42195,"primaryZone":"MP",
     "humanReadable":"Goal 3:45 (5:20/km). Km 0-5: 5:25-5:28. Km 5-30: 5:18-5:22, HR 158 or below. Km 30+: hold or push if HR allows. Gel every 30 min.","completed":False}]})

weeks=[]; tot_run=[]
for n in range(1,13):
    phase,focus,rec,days=W[n]
    ws=start+dt.timedelta(weeks=n-1)
    dl=[]; rk=0; rh=0; bh=0; rs=0; bs=0
    for i in range(7):
        d=ws+dt.timedelta(days=i)
        wl=days.get(i,[rest(f"w{n}-{i}")])
        for w in wl:
            if w["sport"]=="run": rk+=(w.get("distanceMeters") or 0)/1000; rh+=w.get("durationMinutes",0)/60; rs+=1
            if w["sport"]=="bike": bh+=w["durationMinutes"]/60; bs+=1
        dl.append({"date":d.isoformat(),"dayOfWeek":DAYS[i],"workouts":wl})
    weeks.append({"weekNumber":n,"startDate":ws.isoformat(),"endDate":(ws+dt.timedelta(days=6)).isoformat(),
      "phase":phase,"focus":focus,"targetHours":round(rh+bh,1),"isRecoveryWeek":rec,"days":dl,
      "summary":{"totalHours":round(rh+bh,1),"bySport":{"run":{"sessions":rs,"hours":round(rh,1),"km":round(rk,1)},
        **({"bike":{"sessions":bs,"hours":round(bh,1),"km":0}} if bs else {})}}})
    tot_run.append(round(rk,1))

L=166
zones=[(1,"Recovery",0,81),(2,"Aerobic",81,89),(3,"Tempo",90,93),(4,"Sub-threshold",94,99),(5,"Threshold (5a)",100,102),(6,"VO2max (5b)",103,106)]
plan={"version":"1.0","meta":{"id":"tmm-2027","athlete":"Jayesh","event":"Tata Mumbai Marathon 2027","eventDate":"2027-01-17",
 "planStartDate":"2026-10-26","planEndDate":"2027-01-17","createdAt":"2026-10-29T00:00:00Z","updatedAt":"2026-10-29T00:00:00Z",
 "totalWeeks":12,"generatedBy":"Claude Coach (coros-coach)"},
 "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
 "assessment":{"foundation":{"raceHistory":["Leh/Ladakh marathon Sep 2026 (42.5 km, 6:01, altitude)","Gurgaon triathlon Oct 2026"],
   "peakTrainingLoad":9,"foundationLevel":"intermediate","yearsInSport":2},
  "currentForm":{"weeklyVolume":{"total":7,"run":1.5,"bike":1,"swim":0.7},"longestSessions":{"run":12.7,"bike":15},"consistency":3},
  "strengths":[{"sport":"run","evidence":"Marathon finished Sep 2026; 50-60 km weeks in Aug/Sep; VO2max 54"},
               {"sport":"strength","evidence":"4-5 lifting sessions/wk consistently"}],
  "limiters":[{"sport":"run","evidence":"Last 3 wks only 12-16 km/wk; LT pace 5:18/km is slower than sub-3:30 MP (4:58)"}],
  "constraints":["4 runs/wk: Tue, Wed, Fri, Sun","Heavy lifting Mon (press) / Wed (bench) / Fri (squat) / Sat (deadlift), deload every 4th wk",
    "Pool access ending — no swim","Gurgaon heat/pollution: HR caps over pace","Goal revised: sub-3:30 → 3:45 (stretch 3:40)"]},
 "zones":{"run":{"hr":{"lthr":L,"zones":[{"zone":z,"name":nm,"percentLow":lo,"percentHigh":hi,
   "hrLow":round(L*lo/100),"hrHigh":round(L*hi/100)} for z,nm,lo,hi in zones]},
   "pace":{"thresholdPace":"5:18/km","easy":pr(E),"marathon":pr(MP),"threshold":pr(T),"interval":pr(I)}}},
 "phases":[
  {"name":"Rebuild","startWeek":1,"endWeek":2,"focus":"Restore 5 runs/wk after 3 low weeks","weeklyHoursRange":{"low":2.5,"high":4},
   "keyWorkouts":["Long run 14-16k"],"physiologicalGoals":["Re-establish frequency","Tendon/joint re-loading"]},
  {"name":"Base","startWeek":3,"endWeek":4,"focus":"Aerobic volume + threshold","weeklyHoursRange":{"low":4,"high":5},
   "keyWorkouts":["3x8min T","Long 18k","30-min LT test"],"physiologicalGoals":["Raise LT pace","Aerobic base"]},
  {"name":"Build","startWeek":5,"endWeek":8,"focus":"Marathon-specific: MP volume, intervals, long-run fuelling","weeklyHoursRange":{"low":4.5,"high":6.5},
   "keyWorkouts":["MP 6-8k","Long 20-25k w/ MP","LT retest wk 8"],"physiologicalGoals":["MP economy","Glycogen sparing","Gut training"]},
  {"name":"Peak","startWeek":9,"endWeek":10,"focus":"Highest volume + race simulation","weeklyHoursRange":{"low":7,"high":7.5},
   "keyWorkouts":["MP 10k","32k w/ 3x5k MP"],"physiologicalGoals":["Fatigue resistance at MP"]},
  {"name":"Taper","startWeek":11,"endWeek":12,"focus":"Shed fatigue, keep sharpness","weeklyHoursRange":{"low":3,"high":5},
   "keyWorkouts":["MP 8k","MP sharpener"],"physiologicalGoals":["Supercompensation"]}],
 "weeks":weeks,
 "raceStrategy":{"event":{"name":"Tata Mumbai Marathon","date":"2027-01-17","type":"marathon","distances":{"run":42.2}},
  "pacing":{"run":{"targetPace":"5:18-5:22/km (goal 3:45); 5:13/km if wk-8 LT test ≤5:05/km (3:40)","targetHR":"≤158 to km 30, then free",
   "notes":"Km 0-5 at 5:25-5:28 (crowded, dark, humid). Don't chase pace on Bandra-Worli Sea Link incline — hold effort. Bank nothing. "
           "Expect late-race rise toward Peddar Road / Marine Drive and rising heat after ~7 am: if temp >24°C / very humid, add 5-10 s/km and race HR, not pace. Halfway target ~1:53."}},
  "nutrition":{"preRace":"Wake 3:00-3:15. 2.5-3 h before: 100-150 g carbs low-fibre (white bread/jam/banana/rice) + 500 ml fluid w/ electrolytes. Gel 15 min pre-start.",
   "during":{"carbsPerHour":60,"fluidPerHour":"400-700 ml w/ electrolytes (humid — salt matters)","products":["Gel every 30 min (same brand as long runs)","Sip water/electrolyte at most stations"]},
   "notes":"Rehearse exact fuel on wk 7, 9, 10 long runs. Carb load Fri-Sat (8-10 g/kg/day). Nothing new on race day."},
  "taper":{"startDate":"2027-01-04","volumeReduction":35,"notes":"Wk 11 ~-30%, wk 12 ~-55% excl race. Keep MP touches. Lower-body lifting light wk 11, none wk 12."}}}
out=os.path.join(ROOT, "plans/jayesh-345.json")
json.dump(plan,open(out,"w"),indent=1,ensure_ascii=False)
print("run km/wk:",tot_run)
for w in weeks: print(w["weekNumber"],w["startDate"],w["phase"],w["summary"])
