#!/bin/bash

# get particles
grep "PtclTag" $1 | sed -e 's/\([a-z]*\) *PtclTag.*/\1(PTCL)\t\1/g' > memorize.txt

# get pronouns
grep "(PRO.*Enclitic" $1 | sed -e 's/\([a-z]*(PRO\.[A-Za-z_]*\.[0-9][A-Z][a-z])\):\([a-z]*\) *Enclitic; /\1\t\2\n/g' >> memorize.txt

# get demonstratives
grep "(DEM.PRO.Abs.Sg):" $1 | sed -e "s/\([a-z']*(DEM\.PRO\.Abs\.Sg)\):\([a-z']*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.PRO.Abs.Sg)

grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[Rel\.Sg\]\t\1m\n/g" >> memorize.txt # (DEM.PRO)^[Rel.Sg]
grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[Abl_Mod\.Sg\]\t\1meng\n/g" >> memorize.txt # (DEM.PRO)^[Abl_Mod.Sg]
grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[Loc\.Sg\]\t\1mi\n/g" >> memorize.txt # (DEM.PRO)^[Loc.Sg]
grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[All\.Sg\]\t\1mun\n/g" >> memorize.txt # (DEM.PRO)^[All.Sg]
grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[Prl\.Sg\]\t\1kun\n/g" >> memorize.txt # (DEM.PRO)^[Prl.Sg]
grep "(DEM\.PRO):.*DemProSg" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProSg; /\1(DEM\.PRO)\^\[Equ\.Sg\]\t\1tun\n/g" >> memorize.txt # (DEM.PRO)^[Equ.Sg]

grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[AbsRel\.Pl\]\t\1t\n/g" >> memorize.txt # (DEM.PRO)^[AbsRel.Pl]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Abl_Mod\.Pl\]\t\1neng\n/g" >> memorize.txt # (DEM.PRO)^[Abl_Mod.Pl]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Loc\.Pl\]\t\1ni\n/g" >> memorize.txt # (DEM.PRO)^[Loc.Pl]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[All\.Pl\]\t\1nun\n/g" >> memorize.txt # (DEM.PRO)^[All.Pl]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Prl\.Pl\]\t\1tgun\n/g" >> memorize.txt # (DEM.PRO)^[Prl.Pl]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Equ\.Pl\]\t\1stun\n/g" >> memorize.txt # (DEM.PRO)^[Equ.Pl]

grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[AbsRel\.Du\]\t\1k\n/g" >> memorize.txt # (DEM.PRO)^[AbsRel.Du]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Abl_Mod\.Du\]\t\1gneng\n/g" >> memorize.txt # (DEM.PRO)^[Abl_Mod.Du]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Loc\.Du\]\t\1gni\n/g" >> memorize.txt # (DEM.PRO)^[Loc.Du]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[All\.Du\]\t\1ginun\n/g" >> memorize.txt # (DEM.PRO)^[All.Du]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Prl\.Du\]\t\1gnegun\n/g" >> memorize.txt # (DEM.PRO)^[Prl.Du]
grep "(DEM\.PRO):.*DemProPD" $1 | sed -e "s/[a-z']*(DEM\.PRO):\([a-z']*\) *DemProPD; /\1(DEM\.PRO)\^\[Equ\.Du\]\t\1gestun\n/g" >> memorize.txt # (DEM.PRO)^[Equ.Du]

grep "(DEM.ADV):" $1 | sed -e "s/\([a-z']*(DEM\.ADV)\):\([a-z']*\) *DemAdvPB; /\1\t\2\n/g" >> memorize.txt # (DEM.ADV)

grep "(DEM.ADV.Loc):" $1 | sed -e "s/\([a-z']*(DEM\.ADV.Loc)\):\([a-z']*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.ADV.Loc)
grep "(DEM.ADV.All):" $1 | sed -e "s/\([a-z']*(DEM\.ADV.All)\):\([a-z']*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.ADV.All)
grep "(DEM.ADV.Prl):" $1 | sed -e "s/\([a-z']*(DEM\.ADV.Prl)\):\([a-z']*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.ADV.Prl)
grep "(DEM.ADV.Abl_Mod):" $1 | sed -e "s/\([a-z']*(DEM\.ADV.Abl_Mod)\):\([a-z']*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.ADV.Abl_Mod)

grep "(DEM.VOC.Sg):" $1 | sed -e "s/\([a-z']*(DEM.VOC\.Sg)\):\([a-z]*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.VOC.Sg)
grep "(DEM.VOC.Pl):" $1 | sed -e "s/\([a-z']*(DEM.VOC\.Pl)\):\([a-z]*\) *Enclitic; /\1\t\2\n/g" >> memorize.txt # (DEM.VOC.Pl)

# cleanup
sed -i 's/^ *//' memorize.txt
sed -i 's/ *!.*//g' memorize.txt
sed -i '/^$/d' memorize.txt
sed -i '/^[[:space:]]*$/d' memorize.txt
