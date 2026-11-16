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

INTERIM="HR 150 max (interim until 24 Nov test; old LTHR 166 likely stale). If 150 forces you slower than 7:00/km, run 6:40-6:55/km instead. NEVER faster than 6:40/km"
POST="HR cap = 88% of NEW LTHR from 24 Nov test (150 until reset) + pace band set from new LT pace. Run in the band; HR over cap = slow down. NEVER faster than the band"
RETURN="Return from illness: HR 145 max, 6:50/km or slower. Fever, aches, chest tightness or dizziness = stop and walk home"
EASY_RULE=INTERIM
def easy(id,km,strides=False,note="",opt=False):
    mins=km*385/60+(3 if strides else 0)
    h=f"{km} km easy. {EASY_RULE}"
    if strides: h+="\nThen 6x20s strides (fast, relaxed, ~4:30/km) w/ 40s walk"
    if note: h+="\n"+note
    return wo(id,("Optional easy" if opt else "Easy")+f" {km}k"+(" + strides" if strides else ""),km,mins,"Zone 2",h,"Aerobic volume. Conversational.","endurance" if not strides else "endurance")
LONG_W3="Long-run rule (wk 3 only, until 17 Nov test): HR avg 150-156, hard ceiling 160 on hills/late. Pace 6:30-6:50/km, NEVER faster than 6:30. First 3 km HR <=150 as warm-up, then settle into the band. HR past 160 = slow down"
def long(id,km,mp_km=0,note="",rule=None):
    EASY_RULE=rule or globals()["EASY_RULE"]
    e_km=km-mp_km
    mins=e_km*385/60+mp_km*322/60
    h=f"{km} km total. "
    if mp_km: h+=f"First {e_km-2 if mp_km else e_km} km easy ({EASY_RULE}) → {mp_km} km @ MP {pr(MP)} (by pace) → 2 km easy"
    else: h+="Easy. "+EASY_RULE
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
def prog(id,e_km,s_km,m_km):
    km=e_km+s_km+m_km+1
    mins=(e_km+1)*385/60+s_km*350/60+m_km*322/60
    return wo(id,f"Progression {km}k",km,mins,"Z2 → MP",
      f"{e_km} km easy (cap per new LTHR, never faster than easy band)\n{s_km} km steady @ 5:45-5:55/km (HR ≤155)\n{m_km} km @ MP {pr(MP)} (HR ≤162). NEVER faster than 5:18, even if your partner pushes\n1 km easy CD",
      "Key session (replaces the MP session this week). Finish at marathon pace, not faster.","tempo")
def tt(id,note=""):
    return q(id,"30-min threshold test",9,70,"Test",
      "2 km easy WU + 4 strides\n30 min solo all-out-but-even (flat route, early AM)\nRecord: avg pace + avg HR of LAST 20 min = new LT pace / LTHR → I re-set MP\n2 km easy CD"+("\n"+note if note else ""),"test")
def rest(id,note="No running. Strength day (your programme).",name="No run — strength"):
    return {"id":id,"sport":"rest","type":"rest","name":name,"description":note,"completed":False}
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
    return {0:rest(f"w{n}-mon","Deadlift + pull day. No run. Cap deadlift at RPE 7-8, quality run tomorrow."),
            2:rest(f"w{n}-wed","Bench + push day. No run."),
            3:rest(f"w{n}-thu","Full rest, no gym."),
            5:rest(f"w{n}-sat","Shoulder press + arms. Upper body only, long run tomorrow.")}[i]
def W4(n,phase,focus,rec,d):
    for i in ((0,3,5) if n<=2 else (0,2,3,5)):
        d.setdefault(i,[R(n,i)])
    wk(n,phase,focus,rec,d)
FRI="Run in the morning, squat later in the day."
W4(1,"Rebuild","Restart on four runs a week. HRV is a little below baseline, so keep it easy",False,{
 0:[rest("w1-mon","Done: strength.")],
 1:[done(wo("w1-tue","Done: 6.5k incl 1k reps",6.6,46,"mixed","Already completed (Oct 27).","endurance"))],
 2:[done(wo("w1-wed","Done: 6k easy",6.1,48,"Zone 2","Already completed (Oct 28).","endurance"))],
 4:[easy("w1-fri",6)],6:[long("w1-sun",14)]})
W4(2,"Rebuild","Four runs a week, first light quality",False,{
 1:[q("w2-tue","Fartlek 8x200m",6.8,42,"Zone 2 + 5b","2 km easy WU\n8x(200 m brisk @ 4:45-4:55/km, about 1 min / 150 m easy jog)\n2 km easy CD","vo2max")],
 2:[easy("w2-wed",6)],4:[mp("w2-fri",3)],6:[long("w2-sun",16)]})
W4(3,"Base","Progression done Tue. Rest of the week easy so Sunday's 18k is truly aerobic",False,{
 1:[done(wo("w3-tue","Done: progression 7k with partner",7.0,47,"Z2 → T","Done (Nov 10). Finished 5:29/km at HR 175, harder than intended. Counts as this week's quality session.","tempo"))],
 3:[easy("w3-thu",7)],4:[easy("w3-fri",7,True)],6:[long("w3-sun",18,0,"",LONG_W3)]})
SICK="No run — sick"; TRIP="No run — trip"
GATE="Only run if you have had 24h+ with no fever (without paracetamol) and no body aches. If not, rest and slide this run a day"
EASY_RULE=RETURN
W4(4,"Base","Sick week (fever 14-15 Nov). Rest, then three short easy runs. Threshold test moved to 24 Nov",True,{
 0:[rest("w4-mon","Sick. Full rest, no gym.",SICK)],
 1:[rest("w4-tue","Sick. Full rest, no gym. Threshold test moved to Tue 24 Nov.",SICK)],
 2:[rest("w4-wed","Rest. 20-30 min walk if the aches are gone.",SICK)],
 3:[easy("w4-thu",4,False,GATE)],
 4:[rest("w4-fri","Rest. No squats this week.","No run — rest")],
 5:[easy("w4-sat",6,False,"Only if Thursday's run felt normal. Light upper-body gym is fine from today.")],
 6:[easy("w4-sun",10,False,"No long run this week. Stop at 8 km if it feels like work.")]})
EASY_RULE=POST
W4(5,"Build","Back to five runs. Threshold test Tue, everything else easy. Long run 16k",False,{
 0:[rest("w5-mon","Deadlift + pull at about 70% load. First full gym day back.")],
 1:[tt("w5-tue","Test only if: 5+ days fever-free, the 3 easy runs felt normal, morning HRV back over 60 and resting HR within 5 of normal. If not, run easy 6k today and test Thu 26 Nov.")],
 2:[easy("w5-wed",4)],3:[easy("w5-thu",7)],4:[easy("w5-fri",5,True)],6:[long("w5-sun",16)]})
W4(6,"Build","VO2 intervals + marathon pace. Long run 21k",False,{
 1:[ints("w6-tue",5,1.0,120)],2:[easy("w6-wed",5)],3:[mp("w6-thu",6)],4:[easy("w6-fri",6,True)],6:[long("w6-sun",21)]})
W4(7,"Build","Longer threshold + progression. Long run 26k",False,{
 1:[thr_km("w7-tue",4,1.6,90)],2:[easy("w7-wed",6)],3:[prog("w7-thu",4,3,3)],4:[easy("w7-fri",6,True)],
 6:[long("w7-sun",26,0,"Full race kit and breakfast rehearsal (wake 3:30, run 5:15)")]})
W4(8,"Peak","Biggest week, moved ahead of the trip. Race rehearsal: 32k with 8k at marathon pace",False,{
 1:[thr_km("w8-tue",3,2.5,120)],2:[easy("w8-wed",6)],3:[easy("w8-thu",7)],4:[easy("w8-fri",5,True)],
 5:[rest("w8-sat","Shoulder press + arms, light. Long run tomorrow.")],
 6:[long("w8-sun",32,8,"Structure: 21 km easy, 4 km at MP, 1 km easy float, 4 km at MP, 2 km easy. Exact race fuel and kit. This is the last 30k+ run.")]})
W4(9,"Peak","Last full week before the trip. Recover from the 32k, one MP session, 20k on Saturday",False,{
 1:[easy("w9-tue",6,False,"Recovery from Sunday's 32k. No quality before Thursday.")],2:[easy("w9-wed",5)],3:[mp("w9-thu",8)],4:[easy("w9-fri",5,True)],
 5:[long("w9-sat",20,0,"Run it Saturday before you leave. If that fails, run 15-20 km on the trip on Sun 27 Dec.")],
 6:[rest("w9-sun","Trip starts. Travel day.",TRIP)]})
W4(10,"Peak","Trip week (27 Dec to 3 Jan) = the down week. Only the weekend long run matters",True,{
 0:[rest("w10-mon","Trip. No run.",TRIP)],
 1:[easy("w10-tue",6,True,"Optional. Skipping it costs nothing this week.",True)],
 2:[rest("w10-wed","Trip. No run.",TRIP)],
 3:[easy("w10-thu",8,False,"Optional. Run it if you get 50 minutes.",True)],
 4:[rest("w10-fri","Trip. No run.",TRIP)],
 5:[long("w10-sat",18,6,"The one run that matters this week. Sat 2 Jan or Sun 3 Jan, whichever fits travel. 15 km minimum if time is short, keep the MP block.")],
 6:[rest("w10-sun","Travel home. Do the long run today if you skipped it yesterday.",TRIP)]})
W4(11,"Taper","Back from the trip. Volume down, intensity stays. Lower-body lifting light",False,{
 0:[rest("w11-mon","Deadlift light (RPE 6), no grinding.")],
 1:[thr_km("w11-tue",3,2,120)],2:[easy("w11-wed",6)],3:[mp("w11-thu",8)],4:[easy("w11-fri",5,True)],
 6:[long("w11-sun",16,5)]})
W4(12,"Race","Race week. No heavy lower-body lifting",False,{
 0:[rest("w12-mon","Upper body only, light. No deadlift.")],
 1:[q("w12-tue","MP sharpener 3x1.6k",9,52,"MP","2 km easy WU\n3x1.6 km @ MP 5:18-5:26/km, 2 min jog between\n2 km easy CD","tempo")],
 2:[easy("w12-wed",5)],
 3:[easy("w12-thu",4,True)],
 4:[rest("w12-fri","Rest. No leg day. Carb loading starts (8-10 g per kg).")],
 5:[rest("w12-sat","Rest or 15 min shakeout. Carb load, bib pickup, kit laid out, sleep early.")],
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
 "planStartDate":"2026-10-26","planEndDate":"2027-01-17","createdAt":"2026-10-29T00:00:00Z","updatedAt":"2026-11-16T00:00:00Z",
 "totalWeeks":12,"generatedBy":"Claude Coach (coros-coach)"},
 "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
 "assessment":{"foundation":{"raceHistory":["Leh/Ladakh marathon Sep 2026 (42.5 km, 6:01, altitude)","Gurgaon triathlon Oct 2026"],
   "peakTrainingLoad":9,"foundationLevel":"intermediate","yearsInSport":2},
  "currentForm":{"weeklyVolume":{"total":7,"run":1.5,"bike":1,"swim":0.7},"longestSessions":{"run":12.7,"bike":15},"consistency":3},
  "strengths":[{"sport":"run","evidence":"Marathon finished Sep 2026; 50-60 km weeks in Aug/Sep; VO2max 54"},
               {"sport":"strength","evidence":"4-5 lifting sessions/wk consistently"}],
  "limiters":[{"sport":"run","evidence":"Last 3 wks only 12-16 km/wk; LT pace 5:18/km is slower than sub-3:30 MP (4:58)"}],
  "constraints":["5 runs/wk from wk 4: Tue quality, Wed easy, Thu MP or progression (alternating), Fri easy + strides, Sun long","Heavy lifting Mon (deadlift) / Wed (bench) / Fri (squat) / Sat (shoulder press); lower body RPE 7-8 max from wk 5","Plan only changes on red flags: HRV <60 two mornings running, RHR 7+ above baseline, pain, illness",
    "Illness 14-16 Nov (fever): wk 3 long run missed, wk 4 rest + easy return","Trip 27 Dec - 3 Jan: 32k moved to 20 Dec, trip week is the down week with one 18k long run","Pool access ending — no swim","Gurgaon heat/pollution: HR caps over pace","COROS LTHR 166 is stale (held 175 on 10 Nov). 24 Nov 30-min test (moved from 17 Nov, illness) sets real LTHR + LT pace; easy runs then pace band + HR ceiling","Non-negotiable: easy = easy, no unplanned runs, no skipped key sessions, run your session not your partner's, gels on every long run 18k+, pain = stop","Goal revised: sub-3:30 → 3:45 (stretch 3:40)"]},
 "zones":{"run":{"hr":{"lthr":L,"zones":[{"zone":z,"name":nm,"percentLow":lo,"percentHigh":hi,
   "hrLow":round(L*lo/100),"hrHigh":round(L*hi/100)} for z,nm,lo,hi in zones]},
   "pace":{"thresholdPace":"5:18/km","easy":"interim: HR ≤150, never faster than 6:40/km; reset by 24 Nov test (pace band + HR cap 88% new LTHR)","marathon":pr(MP),"threshold":pr(T),"interval":pr(I)}}},
 "phases":[
  {"name":"Rebuild","startWeek":1,"endWeek":2,"focus":"Restore 5 runs/wk after 3 low weeks","weeklyHoursRange":{"low":2.5,"high":4},
   "keyWorkouts":["Long run 14-16k"],"physiologicalGoals":["Re-establish frequency","Tendon/joint re-loading"]},
  {"name":"Base","startWeek":3,"endWeek":4,"focus":"Aerobic volume, then illness recovery","weeklyHoursRange":{"low":2,"high":4.5},
   "keyWorkouts":["Progression 7k","Easy return runs"],"physiologicalGoals":["Raise LT pace","Aerobic base"]},
  {"name":"Build","startWeek":5,"endWeek":7,"focus":"LT test, then marathon-specific: MP volume, intervals, long-run fuelling","weeklyHoursRange":{"low":4.5,"high":6.5},
   "keyWorkouts":["30-min LT test 24 Nov","MP 6k","Long 16-26k"],"physiologicalGoals":["MP economy","Glycogen sparing","Gut training"]},
  {"name":"Peak","startWeek":8,"endWeek":10,"focus":"Highest volume + race simulation before the trip, then trip down week","weeklyHoursRange":{"low":3.5,"high":7},
   "keyWorkouts":["32k w/ 2x4k MP (20 Dec)","MP 8k","Trip long run 18k w/ 6k MP"],"physiologicalGoals":["Fatigue resistance at MP"]},
  {"name":"Taper","startWeek":11,"endWeek":12,"focus":"Shed fatigue, keep sharpness","weeklyHoursRange":{"low":3,"high":5},
   "keyWorkouts":["MP 8k","MP sharpener"],"physiologicalGoals":["Supercompensation"]}],
 "weeks":weeks,
 "raceStrategy":{"event":{"name":"Tata Mumbai Marathon","date":"2027-01-17","type":"marathon","distances":{"run":42.2}},
  "pacing":{"run":{"targetPace":"5:18-5:22/km (goal 3:45); 5:13/km only if the 24 Nov test gives LT pace ≤5:05/km and the MP blocks on 20 Dec feel controlled (3:40)","targetHR":"≤158 to km 30, then free",
   "notes":"Km 0-5 at 5:25-5:28 (crowded, dark, humid). Don't chase pace on Bandra-Worli Sea Link incline — hold effort. Bank nothing. "
           "Expect late-race rise toward Peddar Road / Marine Drive and rising heat after ~7 am: if temp >24°C / very humid, add 5-10 s/km and race HR, not pace. Halfway target ~1:53."}},
  "nutrition":{"preRace":"Wake 3:00-3:15. 2.5-3 h before: 100-150 g carbs low-fibre (white bread/jam/banana/rice) + 500 ml fluid w/ electrolytes. Gel 15 min pre-start.",
   "during":{"carbsPerHour":60,"fluidPerHour":"400-700 ml w/ electrolytes (humid — salt matters)","products":["Gel every 30 min (same brand as long runs)","Sip water/electrolyte at most stations"]},
   "notes":"Rehearse exact fuel on wk 7, 8, 9 long runs. Carb load Fri-Sat (8-10 g/kg/day). Nothing new on race day."},
  "taper":{"startDate":"2027-01-04","volumeReduction":35,"notes":"Wk 11 ~-30%, wk 12 ~-55% excl race. Keep MP touches. Lower-body lifting light wk 11, none wk 12."}}}
out=os.path.join(ROOT, "plans/jayesh-345.json")
json.dump(plan,open(out,"w"),indent=1,ensure_ascii=False)
print("run km/wk:",tot_run)
for w in weeks: print(w["weekNumber"],w["startDate"],w["phase"],w["summary"])
