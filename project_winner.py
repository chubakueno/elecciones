from re import U
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
names_partido = {}
dict_votaron = {}
dict_por_contabilizadas = {}
dict_total_jee = {}
dict_procesadas = {}
for i in data:
    if i["TOT_CIUDADANOS_VOTARON"] is None or i["POR_VALIDOS"] is None or i["C_CODI_AGP"] is None:
        continue
    cod_part = i["C_CODI_AGP"]
    names_partido[cod_part] = i["AGRUPACION"]
    ubigeo = i["CCODI_UBIGEO"]
    tot_ciudadanos_votaron = parse_filtered_double(i["TOT_CIUDADANOS_VOTARON"])
    por_validos = parse_filtered_double(i["POR_VALIDOS"])/100.0
    por_contabilizadas = parse_filtered_double(i["POR_ACTAS_CONTABILIZADAS"])/100.0
    total_jee = round(parse_filtered_double(i["TOTAL_JEE"]))
    procesadas = round(parse_filtered_double(i["ACTAS_PROCESADAS"]))
    dict_por_contabilizadas[ubigeo] = por_contabilizadas
    dict_votaron[ubigeo] = tot_ciudadanos_votaron
    dict_total_jee[ubigeo] = total_jee
    dict_procesadas[ubigeo] = procesadas
    tentativo[cod_part] = tentativo.get(
        cod_part, 0) + tot_ciudadanos_votaron*por_validos

ubigeos = sorted(dict_por_contabilizadas.keys())

real_tot = 0
for ubigeo in dict_votaron:
    real_tot += dict_votaron[ubigeo]
print(f"Total: {round(real_tot)} ciudadanos votaron")

estimated_tot = 0
for partido in tentativo:
    estimated_tot += tentativo[partido]
print(f"Total: {round(estimated_tot)} votos tentativos estimados (puede haber pequeno error de redondeo)")

print("\nPorcentaje de actas contabilizadas por ubigeo:")
for ubigeo in ubigeos:
    print("Ubigeo {} con {} ciudadanos que votaron contabilizado al {:05.2F}%".format(ubigeo, round(dict_votaron[ubigeo]), dict_por_contabilizadas[ubigeo]*100))

print("\nActas enviadas al JEE por ubigeo:")
total_envidadas_jee = 0
total_procesadas = 0
for ubigeo in ubigeos:
    total_jee = dict_total_jee[ubigeo]
    print(f"Ubigeo {ubigeo} con {total_jee} actas enviadas al JEE")
    total_envidadas_jee += total_jee
    total_procesadas += dict_procesadas[ubigeo]

print(f"\nTotal procesadas: {total_procesadas}")
print(f"Total enviadas al JEE: {total_envidadas_jee}")
print(f"Porcentaje de actas enviadas al JEE: {round(total_envidadas_jee/total_procesadas*100,2)}%")

print("\nProyeccion:")
for partido in tentativo:
    print("{:05.2F}% {}".format(tentativo[partido]/estimated_tot*100, names_partido[partido]))
