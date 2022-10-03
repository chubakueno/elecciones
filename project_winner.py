from numpy import double
import json
import sys


def parse_filtered_double(x):
    return double(x.replace(',', ''))

json_filename = sys.argv[1]
f = open(json_filename)
data = json.load(f)
f.close()

tentativo = {}
names = {}
votaron = {}
for i in data:
    if i["TOT_CIUDADANOS_VOTARON"] is None or i["POR_VALIDOS"] is None or i["C_CODI_AGP"] is None:
        continue
    cod_part = i["C_CODI_AGP"]
    names[cod_part] = i["AGRUPACION"]
    ubigeo = i["CCODI_UBIGEO"]
    tot_ciudadanos_votaron = parse_filtered_double(i["TOT_CIUDADANOS_VOTARON"])
    por_validos = parse_filtered_double(i["POR_VALIDOS"])/100.0
    votaron[ubigeo] = tot_ciudadanos_votaron
    tentativo[cod_part] = tentativo.get(
        cod_part, 0) + tot_ciudadanos_votaron*por_validos

real_tot = 0
for ubigeo in votaron:
    real_tot += votaron[ubigeo]
print(f"Total: {round(real_tot)} ciudadanos votaron")

estimated_tot = 0
for partido in tentativo:
    estimated_tot += tentativo[partido]
print(f"Total: {round(estimated_tot)} votos tentativos estimados (puede haber pequeno error de redondeo)")

for partido in tentativo:
    print("{:05.2F}%".format(tentativo[partido]/estimated_tot*100, 2), names[partido])
