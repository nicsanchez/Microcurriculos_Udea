from django.shortcuts import render, HttpResponse,get_object_or_404
from .models import Microcurriculum,Unity,Evaluation,Curso,Curso_asignado,Curso_programado,Semestres
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
import collections
import json
# Create your views here.

def core(request):
    if request.method == "POST":
        descripcion_gen = request.POST['descripcion_general']
        proposito = request.POST['proposito']
        metodologia = request.POST['metodologia'] 
        act_asis_oblig = request.POST['actividades_asis_oblig']
        semestre = request.POST['semestre_es']        
        cantidad_generales = int(request.POST["contadorgeneral"])
        cantidad_especificos = int(request.POST["contadorespecifico"])
        cantidad_resumido = int(request.POST["contadoresumido"])
        cantidad_basicas = int(request.POST["contadorbasica"])
        cantidad_complementarias = int(request.POST["contadorcomple"])
        obj_gen = ""
        obj_esp = ""
        cont_resu = ""
        bibliografia_bas = ""
        bibliografia_comp = ""
        for i in range(1,cantidad_generales+1):
            num=str(i)
            objetivo=request.POST['general'+num]   
            obj_gen=obj_gen+" /objgen-"+objetivo+"-/objgen"
        #print("generales :",obj_gen)
        for i in range(1,cantidad_especificos+1):
            num=str(i)
            objetivo=request.POST['especifico'+num]   
            obj_esp=obj_esp+" /objesp-"+objetivo+"-/objesp"
        #print("especificos :",obj_esp)
        for i in range(1,cantidad_resumido+1):
            num=str(i)
            objetivo=request.POST['item'+num]   
            cont_resu=cont_resu+" /contresu-"+objetivo+"-/contresu"
        #print("items :",cont_resu)
        for i in range(1,cantidad_basicas+1):
            num=str(i)
            objetivo=request.POST['basica'+num]   
            bibliografia_bas=bibliografia_bas+" /biblibas-"+objetivo+"-/biblibas"
        #print("basicos :",bibliografia_bas)
        for i in range(1,cantidad_complementarias+1):
            num=str(i)
            objetivo=request.POST['complementaria'+num]   
            bibliografia_comp=bibliografia_comp+" /biblicom-"+objetivo+"-/biblicom"
        #print("complementarios :",bibliografia_comp)
        try:
            version_pensum = int(request.POST['version_p'])
            curso_es = request.POST['curso_es']
            cursoglobal = Curso.objects.get(nombre=curso_es)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=version_pensum)
            curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
            mensaje = 'Ya hay un microcurriculo asignado en el semestre seleccionado'
            return render(request, "core/curso.html",{'mensaje': mensaje})
        except:
            insert = Microcurriculum(descripcion_general=descripcion_gen,proposito=proposito,objetivo_general=obj_gen,objetivo_especifico=obj_esp,contenido_resumido=cont_resu,actividades_asis_oblig=act_asis_oblig,bibliografia_basica=bibliografia_bas,bibliografia_complementaria=bibliografia_comp,metodologia=metodologia)
            insert.save()
            version_pensum = int(request.POST['version_p'])
            curso_es = request.POST['curso_es']
            cursoglobal = Curso.objects.get(nombre=curso_es)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=version_pensum)
            microcurriculos = Microcurriculum.objects.filter(descripcion_general=descripcion_gen,proposito=proposito,objetivo_general=obj_gen,objetivo_especifico=obj_esp,contenido_resumido=cont_resu,actividades_asis_oblig=act_asis_oblig,bibliografia_basica=bibliografia_bas,bibliografia_complementaria=bibliografia_comp,metodologia=metodologia)
            ids = []
            for micro in microcurriculos:
                a = int(micro.id)
                ids.append(a)
            id_microcurriculo = Microcurriculum.objects.get(id=max(ids))  
            insert2 = Curso_programado(id_microcurriculos=id_microcurriculo,id_curso_asignado=curso_asig,semestre=semestre)
            insert2.save()
            cantidad_unidades = int(request.POST["contadorunidad"])
            cantidad_evaluaciones = int(request.POST["contadorevaluacion"])
            for i in range(1,cantidad_unidades+1):
                num=str(i)
                tema=request.POST['temas'+num]
                contador=int(request.POST['subtemas'+num])
                subtema=""
                for j in range(1,contador+1):
                    num2=str(j)
                    subtemai=request.POST['subtemauni'+num+num2]
                    subtema=subtema+" /subin-"+subtemai+"-/subin"
                semana=request.POST['semanas'+num]
                insert = Unity(id_microcurriculos=id_microcurriculo,tema=tema,subtema=subtema,num_semanas=semana)
                insert.save()
            for i in range(1,cantidad_evaluaciones+1):
                num=str(i)
                actividad=request.POST['actividad'+num]
                porcentaje=request.POST['porcentaje'+num]
                fecha=request.POST['fecha'+num]
                insert = Evaluation(id_microcurriculos=id_microcurriculo,actividad=actividad,porcentaje=porcentaje,fecha=fecha)
                insert.save()
            mensaje = 'Se ha agregado un nuevo registro de microcurriculo con éxito'
            return render(request, "core/curso.html",{'mensaje': mensaje})  
    return render(request, "core/index.html")

def curso(request):
    if request.method == "POST":
        if (request.POST['caso']=="cursos"):
            pensum = request.POST['pensum']
            nivel = request.POST['nivel']
            area = request.POST['area']
            cursos = funcion(pensum,nivel,area)
            lista_cursos_json = []
            for curso in cursos:
                s = str(curso.id_curso.nombre)
                lista_cursos_json.append(s)
            return HttpResponse(json.dumps({"data":lista_cursos_json}))
        elif(request.POST['caso']=="vigencias"):
            nombre_c = request.POST['curso']
            pensum = request.POST['pensum']
            desde = request.POST['desde']
            hasta = request.POST['hasta']
            desde_u = int(desde.replace("-", ""))
            hasta_u = int(hasta.replace("-", ""))
            cursoglobal = Curso.objects.get(nombre=nombre_c)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
            id_cursoasig = curso_asig.id
            Cursos_prog = Curso_programado.objects.filter(id_curso_asignado=id_cursoasig)
            lista_cursos_prog_json = []
            lista_ids = []
            lista_semestres = []
            lista_comunes = []
            if(hasta_u >= desde_u):
                for Curso_prog in Cursos_prog:
                    semestre_u = int(Curso_prog.semestre.replace("-", ""))
                    if(semestre_u >= desde_u and semestre_u <= hasta_u):
                        lista_ids.append(str(Curso_prog.id_microcurriculos))
                        lista_semestres.append(str(Curso_prog.semestre))
                lista_comunes=[[k]*v for k, v in collections.Counter(lista_ids).items()]
                x1=0
                x2=len(lista_comunes[0])-1
                a=[]
                b=[]
                semestres = Semestres.objects.all()
                x3=0
                x4=0
                x5=0
                x6=0
                string2=[]
                string3=[]
                for semestre in semestres:
                    b.append(str(semestre.descripcion))
                for i in range(1,len(lista_comunes)+1):
                    a.clear()
                    string2.clear()
                    string3.clear()
                    if(i==len(lista_comunes)):
                        for j in range(x1,x2+1):
                            a.append(lista_semestres[j])
                        a=sorted(a)
                        if(len(a)==1):
                            string2.append(a[0])
                        else:
                            x5=0
                            x6=0    
                            for k in range(0,len(a)-1):
                                x3=0
                                x4=0
                                for l in range(0,len(b)):
                                    if(a[k]==b[l]):
                                        x3=l
                                    elif(a[k+1]==b[l]):
                                        x4=l      
                                if(x4-x3==1):
                                    x6=x6+1
                                    s=' a '
                                elif(k==0):
                                    x5=k+1
                                    x6=k+1
                                    string2.append(a[0])
                                    s=" a "     
                                else:
                                    if(len(a)==2):
                                        x5=k
                                        x6=k+1
                                        s=' , '
                                    else:    
                                        x5=k+1
                                        x6=k+1
                                        s=' a '
                                if(a[x5]==a[x6]):
                                    string2.append(a[x5])
                                else:
                                    string2.append(a[x5]+s+a[x6])    
                    else:
                        for j in range(x1,x2+1):
                            a.append(lista_semestres[j])
                        a=sorted(a)
                        if(len(a)==1):
                            string2.append(a[0])
                        else:
                            x5=0
                            x6=0    
                            for k in range(0,len(a)-1):
                                x3=0
                                x4=0
                                for l in range(0,len(b)):
                                    if(a[k]==b[l]):
                                        x3=l
                                    elif(a[k+1]==b[l]):
                                        x4=l      
                                if(x4-x3==1):
                                    x6=x6+1
                                    s=' a '
                                else:
                                    if(len(a)==2):
                                        x5=k
                                        x6=k+1
                                        s=' , '
                                    elif(k==0):
                                        x5=k+1
                                        x6=k+1
                                        string2.append(a[0])
                                        s=" a " 
                                    else:    
                                        x5=k+1
                                        x6=k+1
                                        s=' a '    
                                if(a[x5]==a[x6]):
                                    string2.append(a[x5])
                                else:
                                    string2.append(a[x5]+s+a[x6])
                        x1=x1+len(lista_comunes[i-1])
                        x2=x2+len(lista_comunes[i])
                    for p in range(0,len(string2)):
                        string3.append(string2[p])
                    aux=0
                    print(string3)
                    for h in range(0,len(string2)-1):
                        if(string2[h][0:6]==string2[h+1][0:6]):
                            string3.pop(h-aux)
                            aux=aux+1
                    cadena=string3[0]
                    for z in range(1,len(string3)):
                        cadena=cadena+' , '+string3[z]
                    print(cadena)
                    lista_cursos_prog_json.append(cadena)
            lista_cursos_prog_json = sorted(lista_cursos_prog_json)
            return HttpResponse(json.dumps({"data":lista_cursos_prog_json}))
        elif(request.POST['caso']=="ultimo"):
            pensum = request.POST['pensum']
            nombre_c = request.POST['curso']
            semestre = request.POST['semestre']
            semestre_es = int(semestre.replace("-",""))
            cursoglobal = Curso.objects.get(nombre=nombre_c)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
            id_cursoasig = curso_asig.id
            Cursos_prog = Curso_programado.objects.filter(id_curso_asignado=id_cursoasig)
            lista = []
            for Curso_prog in Cursos_prog:
                hi=Curso_prog.semestre
                hasta_i = int(hi.replace("-", ""))
                s=str(Curso_prog.semestre)
                lista.append(s) 
            if( not lista ):
                return HttpResponse("No hay un ultimo curso vigente")
            else:
                lista = sorted(lista,reverse=True)
                Cursos_prog = Curso_programado.objects.get(id_curso_asignado=id_cursoasig,semestre=lista[0])
                id_ultimo = Cursos_prog.id
                microcurriculo = Microcurriculum.objects.get(id=Cursos_prog.id_microcurriculos.id)
                try:
                    curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                    return HttpResponse("Ya hay un microcurriculo asignado en el semestre seleccionado")
                except:
                    insert = Curso_programado(id_microcurriculos=microcurriculo,id_curso_asignado=curso_asig,semestre=semestre)
                    insert.save()
                    return HttpResponse("Se actualizo correctamente el microcurriculo del curso")
            
        elif(request.POST['caso']=="renovar"):
            pensum = request.POST['pensum']
            nombre_c = request.POST['curso']
            vigencia = request.POST['vigencia']
            semestre = request.POST['semestre']
            cursoglobal = Curso.objects.get(nombre=nombre_c)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
            curso_asociados = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=vigencia[0:6])
            micro_aso = Microcurriculum.objects.get(id=curso_asociados.id_microcurriculos.id)
            try:
                curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                return HttpResponse("Ya hay un microcurriculo asignado en el semestre seleccionado")
            except:
                insert = Curso_programado(id_microcurriculos=micro_aso,id_curso_asignado=curso_asig,semestre=semestre)
                insert.save()
                return HttpResponse("Se renovó correctamente el microcurriculo del curso")
    semestres = Semestres.objects.all()
    return render(request, "core/curso.html",{'semestres':semestres})

def asignar(request):
    if request.method == "POST":
        if (request.POST['caso']=="cursos"):
            pensum = request.POST['pensum']
            nivel = request.POST['nivel']
            area = request.POST['area']
            cursos = funcion(pensum,nivel,area)
            lista_cursos_json = []
            for curso in cursos:
                s = str(curso.id_curso.nombre)
                lista_cursos_json.append(s)
            return HttpResponse(json.dumps({"data":lista_cursos_json}))
        elif(request.POST['caso']=="vigencias"):
            nombre_c = request.POST['curso']
            pensum = request.POST['pensum']
            desde = request.POST['desde']
            hasta = request.POST['hasta']
            desde_u = int(desde.replace("-", ""))
            hasta_u = int(hasta.replace("-", ""))
            cursoglobal = Curso.objects.get(nombre=nombre_c)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
            id_cursoasig = curso_asig.id
            Cursos_prog = Curso_programado.objects.filter(id_curso_asignado=id_cursoasig)
            lista_cursos_prog_json = []
            lista_ids = []
            lista_semestres = []
            lista_comunes = []
            if(hasta_u > desde_u):
                for Curso_prog in Cursos_prog:
                    semestre_u = int(Curso_prog.semestre.replace("-", ""))
                    if(semestre_u >= desde_u and semestre_u <= hasta_u):
                        lista_ids.append(str(Curso_prog.id_microcurriculos))
                        lista_semestres.append(str(Curso_prog.semestre))
                lista_comunes=[[k]*v for k, v in collections.Counter(lista_ids).items()]
                x1=0
                x2=len(lista_comunes[0])-1
                a=[]
                b=[]
                semestres = Semestres.objects.all()
                x3=0
                x4=0
                x5=0
                x6=0
                string2=[]
                string3=[]
                for semestre in semestres:
                    b.append(str(semestre.descripcion))
                for i in range(1,len(lista_comunes)+1):
                    a.clear()
                    string2.clear()
                    string3.clear()
                    if(i==len(lista_comunes)):
                        for j in range(x1,x2+1):
                            a.append(lista_semestres[j])
                        a=sorted(a)
                        if(len(a)==1):
                            string2.append(a[0])
                        else:
                            x5=0
                            x6=0    
                            for k in range(0,len(a)-1):
                                x3=0
                                x4=0
                                for l in range(0,len(b)):
                                    if(a[k]==b[l]):
                                        x3=l
                                    elif(a[k+1]==b[l]):
                                        x4=l      
                                if(x4-x3==1):
                                    x6=x6+1
                                    s=' a '
                                elif(k==0):
                                    x5=k+1
                                    x6=k+1
                                    string2.append(a[0])
                                    s=" a "     
                                else:
                                    if(len(a)==2):
                                        x5=k
                                        x6=k+1
                                        s=' , '
                                    else:    
                                        x5=k+1
                                        x6=k+1
                                        s=' a '
                                if(a[x5]==a[x6]):
                                    string2.append(a[x5])
                                else:
                                    string2.append(a[x5]+s+a[x6])    
                    else:
                        for j in range(x1,x2+1):
                            a.append(lista_semestres[j])
                        a=sorted(a)
                        if(len(a)==1):
                            string2.append(a[0])
                        else:
                            x5=0
                            x6=0    
                            for k in range(0,len(a)-1):
                                x3=0
                                x4=0
                                for l in range(0,len(b)):
                                    if(a[k]==b[l]):
                                        x3=l
                                    elif(a[k+1]==b[l]):
                                        x4=l      
                                if(x4-x3==1):
                                    x6=x6+1
                                    s=' a '
                                else:
                                    if(len(a)==2):
                                        x5=k
                                        x6=k+1
                                        s=' , '
                                    elif(k==0):
                                        x5=k+1
                                        x6=k+1
                                        string2.append(a[0])
                                        s=" a " 
                                    else:    
                                        x5=k+1
                                        x6=k+1
                                        s=' a '    
                                if(a[x5]==a[x6]):
                                    string2.append(a[x5])
                                else:
                                    string2.append(a[x5]+s+a[x6])
                        x1=x1+len(lista_comunes[i-1])
                        x2=x2+len(lista_comunes[i])
                    for p in range(0,len(string2)):
                        string3.append(string2[p])
                    aux=0
                    print(string3)
                    for h in range(0,len(string2)-1):
                        if(string2[h][0:6]==string2[h+1][0:6]):
                            string3.pop(h-aux)
                            aux=aux+1
                    cadena=string3[0]
                    for z in range(1,len(string3)):
                        cadena=cadena+' , '+string3[z]
                    print(cadena)
                    lista_cursos_prog_json.append(cadena)
            lista_cursos_prog_json = sorted(lista_cursos_prog_json)
            return HttpResponse(json.dumps({"data":lista_cursos_prog_json}))
        elif(request.POST['caso']=="asignar"):
            #curso al que se le a asignar el micro
            pensum_e = request.POST['version_p']
            curso_e = request.POST['curso_es']
            semestre_e = request.POST['semestre_es']
            #curso del que pertenece el micro
            pensum_d = request.POST['version_pensum']
            curso_d = request.POST['curso']
            vigencia_d = request.POST['vigencia']
            #curso delcual pertenece el microcurriculo
            cursoglobal = Curso.objects.get(nombre=curso_d)
            id_cursoglobal = cursoglobal.id
            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum_d)
            curso_asociados = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=vigencia_d[0:6])
            micro_aso = Microcurriculum.objects.get(id=curso_asociados.id_microcurriculos.id)
            #curso al que se la va a hacer la asignacion
            cursoglobal2 = Curso.objects.get(nombre=curso_e)
            id_cursoglobal2 = cursoglobal2.id
            curso_asig2 = Curso_asignado.objects.get(id_curso=id_cursoglobal2,version_pensum=pensum_e)
            try:
                curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig2,semestre=semestre_e)
                return HttpResponse("Ya hay un microcurriculo asignado en el semestre seleccionado")
            except:
                insert = Curso_programado(id_microcurriculos=micro_aso,id_curso_asignado=curso_asig2,semestre=semestre_e)
                insert.save()
                return HttpResponse("Se asignó el curso correctamente")         

    semestres = Semestres.objects.all()
    return render(request, "core/asignar.html",{'semestres':semestres})

def funcion(a,b,c):
    #SOLO PENSUM
    if (a != "Seleccione" and b=="Seleccione" and c=="Seleccione"):
        return Curso_asignado.objects.filter(version_pensum=a)
    #PENSUM Y NIVEL    
    elif (a != "Seleccione" and b!="Seleccione" and c=="Seleccione"):
        return Curso_asignado.objects.filter(version_pensum=a,nivel=b)
    #PENSUM, NIVEL Y AREA    
    elif (a != "Seleccione" and b!="Seleccione" and c!="Seleccione"):
        return Curso_asignado.objects.filter(version_pensum=a,nivel=b,area=c)
    #SOLO NIVEL    
    elif (a == "Seleccione" and b!="Seleccione" and c=="Seleccione"):
        return Curso_asignado.objects.filter(nivel=b)
    #NIVEL Y AREA    
    elif (a == "Seleccione" and b!="Seleccione" and c!="Seleccione"):
        return Curso_asignado.objects.filter(nivel=b,area=c)
    #SOLO AREA    
    elif (a == "Seleccione" and b=="Seleccione" and c!="Seleccione"):
        return Curso_asignado.objects.filter(area=c)
    #PENSUM Y AREA    
    elif (a != "Seleccione" and b=="Seleccione" and c!="Seleccione"):
        return Curso_asignado.objects.filter(version_pensum=a,area=c)
        
        