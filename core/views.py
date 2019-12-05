from django.shortcuts import render, HttpResponse,get_object_or_404,redirect
from .models import Microcurriculum,Unity,Evaluation,Curso,Curso_asignado,Curso_programado,Semestres,Microcurriculum_2,Unity_2,Evaluation_2,Solicitud
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.http import FileResponse,Http404
import collections
import json
import base64
import os
from subprocess import call
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
# Create your views here.
def logout(request):
    do_logout(request)
    return redirect('/login')
def login(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)     
            if user is not None:
                do_login(request, user)
                return redirect('/nucleo')
    return render(request, "core/login.html", {'form': form})                

def nuevo1(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):    
            semestres = Semestres.objects.all()
            return render(request, "core/nuevo1.html",{'semestres':semestres})
        else:
            return redirect('/nucleo')    
    return redirect('/login')

def nuevo2(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):    
            semestres = Semestres.objects.all()
            return render(request, "core/nuevo2.html",{'semestres':semestres})
        return redirect('/nucleo')    
    return redirect('/login')

def nuevo3(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):    
            semestres = Semestres.objects.all()
            return render(request, "core/nuevo3.html",{'semestres':semestres})    
        else:
            return redirect('/nucleo')    
    return redirect('/login')
def nuevo4(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):            
            semestres = Semestres.objects.all()
            return render(request, "core/nuevo4.html",{'semestres':semestres})        
        else:
            return redirect('/nucleo')
    return redirect('/login')        
def visualizar(request):
    if request.user.is_authenticated:
        semestres = Semestres.objects.all()
        return render(request, "core/visualizar.html",{'semestres':semestres})
    return redirect('/login')        

def editar(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):
            semestres = Semestres.objects.all()
            return render(request, "core/editar.html",{'semestres':semestres})
        else:
            return redirect('/nucleo')
    return redirect('/login')        

def crear2(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):    
            if request.method == "POST":
                if request.POST['caso']=="confirmacion":
                    pensum = request.POST['pensum']
                    nombre_c = request.POST['curso']
                    cursoglobal = Curso.objects.get(nombre=nombre_c)
                    id_cursoglobal = cursoglobal.id
                    curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                    curso_asociado = Curso_programado.objects.filter(id_curso_asignado=curso_asig)
                    if(len(curso_asociado)==0):
                        return HttpResponse("false")
                    elif(len(curso_asociado)==1):
                        return HttpResponse("true1")
                    else:
                        return HttpResponse("true")    
            semestres = Semestres.objects.all()
            return render(request, "core/crear.html",{'semestres':semestres})
        else:
            return redirect('/nucleo')
    return redirect('/login')        

def nucleo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['caso']=="nuevopdf":
                pensum = request.POST['pensum']
                nombre_c = request.POST['curso']
                vigencia = request.POST['vigencia']
                cursoglobal=Curso.objects.get(nombre=nombre_c)
                #Datos extraidos de la base de datos curso
                codicur=cursoglobal.codigo
                nomcur=cursoglobal.nombre
                credicur=str(cursoglobal.num_creditos)
                #Datos extraidos de la base de datos curso asignado
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                hoteo=str(curso_asig.horas_t)
                hoteopr=str(curso_asig.horas_tp)
                hoprac=str(curso_asig.horas_p)
                if(curso_asig.validable==True):
                    valcur="Si"
                else:
                    valcur="No"
                if(curso_asig.habilitable==True):
                    habcur="Si"
                else:
                    habcur="No"
                if(curso_asig.clasificable==True):
                    clascur="Si"
                else:
                    clascur="No"        
                vigencur=vigencia
                semcur=str(curso_asig.nivel)
                #preguntar semanas donde esta
                semncur="16"
                areacur=curso_asig.area
                progrcur=curso_asig.id_programa.nombre_progr
                precur=curso_asig.prereq
                corrcur=curso_asig.correq
                justificacion=procesos('des_gen',request)
                propcur=procesos('proposito',request)
                metodocur=procesos('metodologia',request)
                actiasiscur=procesos('activ_oblig',request)
                objgeni=request.POST['generales']
                objgeni=cadenas(objgeni,",a,")
                objespi=request.POST['especificos']
                objespi=cadenas(objespi,",a,")
                itemires=request.POST['items']
                itemires=cadenas(itemires,",a,")
                biblbasi=request.POST['basicas']
                biblbasi=cadenas(biblbasi,",a,")
                biblcompi=request.POST['complemen']
                biblcompi=cadenas(biblcompi,",a,")
                actividadescuri=request.POST['actividadescuri']
                unitys=request.POST['unidades']
                unidades=""
                if(unitys=='No ha agregado este campo'):
                    unidades=unitys
                else:    
                    unitys=unitys.split("\n")
                    for i in range(0,len(unitys)-1):
                        a=unitys[i].split("&/&")
                        unidades=unidades+"\\begin{tabular}{R{0.16\\textwidth} L{0.7\\textwidth}} \n \\\\ \n\\toprule \\textbf{Unidad No. "+a[0]+"} & "+a[1]+" \n \\\\ \n\midrule\\textbf{Subtemas} & \n\\begin{description}\n "+a[2]+"\n\end{description}\n \\\\ \n\\textbf{Semanas} & "+a[3]+" \n\end{tabular} \n \\\\ \n "
                generate_pdf(codicur,nomcur,hoteo,hoteopr,hoprac,valcur,habcur,clascur,vigencur,semcur,semncur,areacur,credicur,progrcur,propcur,justificacion,precur,corrcur,objgeni,objespi,itemires,metodocur,actiasiscur,biblbasi,biblcompi,actividadescuri,unidades)
                with open("salida.pdf", "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
                a=str(encoded_string)
                a=a.replace("b'","")
                a=a.replace("'","")
                return HttpResponse(a)
        semestres = Semestres.objects.all()
        return render(request, "core/nucleo.html",{'semestres':semestres})
    return redirect('/login')        

def core(request):
    if request.user.is_authenticated:
        if (str(request.user.groups.all()[0])=='Validador' or str(request.user.groups.all()[0])=='Digitador'):    
            if request.method == "POST":
                if request.POST['caso']=="nuevo" or request.POST['caso']=="editar":
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
                        obj_gen=obj_gen+" /objgen- "+objetivo
                    for i in range(1,cantidad_especificos+1):
                        num=str(i)
                        objetivo=request.POST['especifico'+num]   
                        obj_esp=obj_esp+" /objesp- "+objetivo
                    for i in range(1,cantidad_resumido+1):
                        num=str(i)
                        objetivo=request.POST['item'+num]   
                        cont_resu=cont_resu+" /contresu- "+objetivo
                    for i in range(1,cantidad_basicas+1):
                        num=str(i)
                        objetivo=request.POST['basica'+num]   
                        bibliografia_bas=bibliografia_bas+" /biblibas- "+objetivo
                    for i in range(1,cantidad_complementarias+1):
                        num=str(i)
                        objetivo=request.POST['complementaria'+num]   
                        bibliografia_comp=bibliografia_comp+" /biblicom- "+objetivo
                    if request.POST['caso']=="nuevo":
                        try:
                            version_pensum = int(request.POST['version_p'])
                            curso_es = request.POST['curso_es']
                            cursoglobal = Curso.objects.get(nombre=curso_es)
                            id_cursoglobal = cursoglobal.id
                            curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=version_pensum)
                            curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                            mensaje = 'Ya hay un microcurriculo asignado en el semestre seleccionado'
                            return render(request, "core/nucleo.html",{'mensaje': mensaje})
                        except:
                            if (str(request.user.groups.all()[0])=='Validador'): 
                                #Se inserta en la base de datos real para el validador y se asigna al curso escogido
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
                            elif(str(request.user.groups.all()[0])=='Digitador'):
                                #Se inserta en la base de datos fantasma para el digitador
                                insert = Microcurriculum_2(descripcion_general=descripcion_gen,proposito=proposito,objetivo_general=obj_gen,objetivo_especifico=obj_esp,contenido_resumido=cont_resu,actividades_asis_oblig=act_asis_oblig,bibliografia_basica=bibliografia_bas,bibliografia_complementaria=bibliografia_comp,metodologia=metodologia)
                                insert.save()
                                microcurriculos = Microcurriculum_2.objects.filter(descripcion_general=descripcion_gen,proposito=proposito,objetivo_general=obj_gen,objetivo_especifico=obj_esp,contenido_resumido=cont_resu,actividades_asis_oblig=act_asis_oblig,bibliografia_basica=bibliografia_bas,bibliografia_complementaria=bibliografia_comp,metodologia=metodologia)
                                ids = []
                                for micro in microcurriculos:
                                    a = int(micro.id)
                                    ids.append(a)
                                id_microcurriculo = Microcurriculum_2.objects.get(id=max(ids))
                                descripcion=request.POST['Descripcion']
                                curso_d=request.POST['curso_es']
                                pensum_d=request.POST['version_p']
                                curso_p=request.POST['curso_es2']
                                pensum_p=request.POST['version_p2']
                                semestre=request.POST['semestre_es']
                                user_p=str(request.user.first_name)+' '+str(request.user.last_name)
                                insert2=Solicitud(soli='Crear',descripcion=descripcion,curso_destino=curso_d,pensum_destino=pensum_d,curso_propietario=curso_p,pensum_propietario=pensum_p,semestre_asignar=semestre,microcurriculo=id_microcurriculo,usuario=user_p)
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
                                    subtema=subtema+" /subin- "+subtemai
                                semana=request.POST['semanas'+num]
                                if (str(request.user.groups.all()[0])=='Validador'): 
                                    insert = Unity(id_microcurriculos=id_microcurriculo,tema=tema,subtema=subtema,num_semanas=semana)
                                elif (str(request.user.groups.all()[0])=='Digitador'):
                                    insert = Unity_2(id_microcurriculos=id_microcurriculo,tema=tema,subtema=subtema,num_semanas=semana) 
                                insert.save()
                            for i in range(1,cantidad_evaluaciones+1):
                                num=str(i)
                                actividad=request.POST['actividad'+num]
                                porcentaje=request.POST['porcentaje'+num]
                                fecha=request.POST['fecha'+num]
                                if (str(request.user.groups.all()[0])=='Validador'): 
                                    insert = Evaluation(id_microcurriculos=id_microcurriculo,actividad=actividad,porcentaje=porcentaje,fecha=fecha)
                                elif (str(request.user.groups.all()[0])=='Digitador'):
                                    insert = Evaluation_2(id_microcurriculos=id_microcurriculo,actividad=actividad,porcentaje=porcentaje,fecha=fecha)
                                insert.save()
                            mensaje = 'Se ha agregado un nuevo registro de microcurriculo con éxito'
                            return render(request, "core/nucleo.html",{'mensaje': mensaje})  
                    elif request.POST['caso']=="editar":
                        pensum = int(request.POST['version_p'])
                        nombre_c = request.POST['curso_es']
                        vigencia =request.POST['vigencia_es']
                        semestre = vigencia[0:6]
                        cursoglobal=Curso.objects.get(nombre=nombre_c)
                        id_cursoglobal = cursoglobal.id
                        curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                        curso_asociado = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                        micro_aso = Microcurriculum.objects.get(id=curso_asociado.id_microcurriculos.id)
                        micro_aso.descripcion_general=descripcion_gen
                        micro_aso.proposito=proposito
                        micro_aso.objetivo_general=obj_gen
                        micro_aso.objetivo_especifico=obj_esp
                        micro_aso.contenido_resumido=cont_resu
                        micro_aso.actividades_asis_oblig=act_asis_oblig
                        micro_aso.bibliografia_basica=bibliografia_bas
                        micro_aso.bibliografia_complementaria=bibliografia_comp
                        micro_aso.metodologia=metodologia
                        micro_aso.save(update_fields=['descripcion_general','proposito','objetivo_general','objetivo_especifico','contenido_resumido','actividades_asis_oblig','bibliografia_basica','bibliografia_complementaria','metodologia'])
                        eval_micro=Evaluation.objects.filter(id_microcurriculos=curso_asociado.id_microcurriculos.id)
                        contador=1
                        cont_eval=int(request.POST['contadorevaluacion'])
                        while (contador<cont_eval+1):
                            if(contador<=len(eval_micro)):
                                for evaluacion in eval_micro:
                                    if(contador<cont_eval+1):
                                        evaluacion.actividad=request.POST['actividad'+str(contador)]
                                        evaluacion.porcentaje=request.POST['porcentaje'+str(contador)]
                                        evaluacion.fecha=request.POST['fecha'+str(contador)]
                                        evaluacion.save(update_fields=['actividad','porcentaje','fecha'])
                                    else:
                                        evaluacion.delete()
                                    contador=contador+1
                            else:
                                actividad=request.POST['actividad'+str(contador)]
                                porcentaje=request.POST['porcentaje'+str(contador)]
                                fecha=request.POST['fecha'+str(contador)]
                                insert = Evaluation(id_microcurriculos=micro_aso,actividad=actividad,porcentaje=porcentaje,fecha=fecha)
                                insert.save()
                                contador=contador+1   
                        contador=1
                        cont_uni=int(request.POST['contadorunidad'])
                        unid_micro=Unity.objects.filter(id_microcurriculos=curso_asociado.id_microcurriculos.id)
                        while(contador<cont_uni+1):
                            if(contador<=len(unid_micro)):
                                for unidad in unid_micro:
                                    if(contador<cont_uni+1):
                                        unidad.tema=request.POST['temas'+str(contador)]
                                        unidad.num_semanas=request.POST['semanas'+str(contador)]
                                        contador2=int(request.POST['subtemas'+str(contador)])
                                        subtema=""
                                        for j in range(1,contador2+1):
                                            num2=str(j)
                                            subtemai=request.POST['subtemauni'+str(contador)+num2]
                                            subtema=subtema+" /subin- "+subtemai
                                        unidad.subtema=subtema
                                        unidad.save(update_fields=['tema','subtema','num_semanas'])
                                    else:
                                        unidad.delete()
                                    contador=contador+1        
                            else:
                                tema=request.POST['temas'+str(contador)]
                                semana=request.POST['semanas'+str(contador)]
                                contador2=int(request.POST['subtemas'+str(contador)])
                                subtema=""
                                for j in range(1,contador2+1):
                                    num2=str(j)
                                    subtemai=request.POST['subtemauni'+str(contador)+num2]
                                    subtema=subtema+" /subin- "+subtemai
                                insert = Unity(id_microcurriculos=micro_aso,tema=tema,subtema=subtema,num_semanas=semana)
                                insert.save()
                                contador=contador+1
                        mensaje = 'Se ha editado el microcurriculo con éxito'
                        return render(request, "core/nucleo.html",{'mensaje': mensaje})  
                    
                elif request.POST['caso']=="nuevopdf":
                    pensum = request.POST['pensum']
                    nombre_c = request.POST['curso']
                    vigencia = request.POST['vigencia']
                    cursoglobal=Curso.objects.get(nombre=nombre_c)
                    #Datos extraidos de la base de datos curso
                    codicur=cursoglobal.codigo
                    nomcur=cursoglobal.nombre
                    credicur=str(cursoglobal.num_creditos)
                    #Datos extraidos de la base de datos curso asignado
                    id_cursoglobal = cursoglobal.id
                    curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                    hoteo=str(curso_asig.horas_t)
                    hoteopr=str(curso_asig.horas_tp)
                    hoprac=str(curso_asig.horas_p)
                    if(curso_asig.validable==True):
                        valcur="Si"
                    else:
                        valcur="No"
                    if(curso_asig.habilitable==True):
                        habcur="Si"
                    else:
                        habcur="No"
                    if(curso_asig.clasificable==True):
                        clascur="Si"
                    else:
                        clascur="No"        
                    vigencur=vigencia
                    semcur=str(curso_asig.nivel)
                    #preguntar semanas donde esta
                    semncur="16"
                    areacur=curso_asig.area
                    progrcur=curso_asig.id_programa.nombre_progr
                    precur=curso_asig.prereq
                    corrcur=curso_asig.correq
                    justificacion=procesos('des_gen',request)
                    propcur=procesos('proposito',request)
                    metodocur=procesos('metodologia',request)
                    actiasiscur=procesos('activ_oblig',request)
                    objgeni=request.POST['generales']
                    objgeni=cadenas(objgeni,",a,")
                    objespi=request.POST['especificos']
                    objespi=cadenas(objespi,",a,")
                    itemires=request.POST['items']
                    itemires=cadenas(itemires,",a,")
                    biblbasi=request.POST['basicas']
                    biblbasi=cadenas(biblbasi,",a,")
                    biblcompi=request.POST['complemen']
                    biblcompi=cadenas(biblcompi,",a,")
                    actividadescuri=request.POST['actividadescuri']
                    unitys=request.POST['unidades']
                    unidades=""
                    if(unitys=='No ha agregado este campo'):
                        unidades=unitys
                    else:    
                        unitys=unitys.split("\n")
                        for i in range(0,len(unitys)-1):
                            a=unitys[i].split("&/&")
                            unidades=unidades+"\\begin{tabular}{R{0.16\\textwidth} L{0.7\\textwidth}} \n \\\\ \n\\toprule \\textbf{Unidad No. "+a[0]+"} & "+a[1]+" \n \\\\ \n\midrule\\textbf{Subtemas} & \n\\begin{description}\n "+a[2]+"\n\end{description}\n \\\\ \n\\textbf{Semanas} & "+a[3]+" \n\end{tabular} \n \\\\ \n "
                    generate_pdf(codicur,nomcur,hoteo,hoteopr,hoprac,valcur,habcur,clascur,vigencur,semcur,semncur,areacur,credicur,progrcur,propcur,justificacion,precur,corrcur,objgeni,objespi,itemires,metodocur,actiasiscur,biblbasi,biblcompi,actividadescuri,unidades)
                    with open("salida.pdf", "rb") as pdf_file:
                        encoded_string = base64.b64encode(pdf_file.read())
                    a=str(encoded_string)
                    a=a.replace("b'","")
                    a=a.replace("'","")
                    return HttpResponse(a)
                elif request.POST['caso']=="base" or request.POST['caso']=="ultimo":
                    if request.POST['caso']=="base":
                        pensum = request.POST['pensum']
                        nombre_c = request.POST['curso']
                        vigencia = request.POST['vigencia']
                        semestre = vigencia[0:6]
                        cursoglobal=Curso.objects.get(nombre=nombre_c)
                        id_cursoglobal = cursoglobal.id
                        curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                        curso_asociado = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                    elif request.POST['caso']=="ultimo":
                        pensum = request.POST['pensum']
                        nombre_c = request.POST['curso']
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
                        lista = sorted(lista,reverse=True)
                        curso_asociado = Curso_programado.objects.get(id_curso_asignado=id_cursoasig,semestre=lista[0])
                    micro_aso = Microcurriculum.objects.get(id=curso_asociado.id_microcurriculos.id)
                    evaluaciones=Evaluation.objects.filter(id_microcurriculos=curso_asociado.id_microcurriculos.id)
                    actividades=""
                    porcentajes=""
                    fechas=""
                    temas=""
                    subtemas=""
                    semanas=""
                    unidades=Unity.objects.filter(id_microcurriculos=curso_asociado.id_microcurriculos.id)
                    for unidad in unidades:
                        temas = temas + " /temuni- " + unidad.tema
                        subtemas = subtemas + " /subtemuni- " + str(unidad.subtema)
                        semanas = semanas + " /semauni- " + str(unidad.num_semanas)
                    for evaluacion in evaluaciones:
                        actividades = actividades + " /acteval- " + evaluacion.actividad
                        porcentajes = porcentajes + " /porceval- " + str(evaluacion.porcentaje)
                        fechas = fechas + " /feceval- " + str(evaluacion.fecha)
                    micro={
                        'des_gen':micro_aso.descripcion_general,
                        'proposito':micro_aso.proposito,
                        'metodologia':micro_aso.metodologia,
                        'act_obl':micro_aso.actividades_asis_oblig,
                        'generales':micro_aso.objetivo_general,
                        'especificos':micro_aso.objetivo_especifico,
                        'resumido':micro_aso.contenido_resumido,
                        'basica':micro_aso.bibliografia_basica,
                        'complementaria':micro_aso.bibliografia_complementaria,
                        'actividad':actividades,
                        'porcentaje':porcentajes,
                        'fecha':fechas,
                        'temas':temas,
                        'subtemas':subtemas,
                        'semanas':semanas
                        }
                    micro2=json.dumps(micro)
                    return HttpResponse(micro2)   
            return render(request, "core/index.html")
        else:
            return redirect("/nucleo")
    return redirect('/login')        

def curso(request):
    if request.user.is_authenticated:
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
            elif(request.POST['caso']=="verificacion"):
                pensum = request.POST['pensum']
                semestre = request.POST['semestre']
                nombre_c = request.POST['curso']
                cursoglobal = Curso.objects.get(nombre=nombre_c)
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                try:
                    curso_asociado = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                    return HttpResponse("false")
                except:
                    return HttpResponse("true")
            elif(request.POST['caso']=="editar"):
                pensum = request.POST['pensum']
                semestre = request.POST['semestre']
                nombre_c = request.POST['curso']
                cursoglobal = Curso.objects.get(nombre=nombre_c)
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                try:
                    curso_asociado = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                    return HttpResponse("false")
                except:
                    return HttpResponse("true")        
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
                        return HttpResponse("Se asignó correctamente el ultimo microcurriculo vigente al semestre seleccionado")
            elif(request.POST['caso']=="ultimo2"):
                pensums = request.POST['pensums'].split(" /pencur- ")
                nombre_cs = request.POST['cursos'].split(" /cursel- ")
                semestre = request.POST['semestre']
                semestre_es = int(semestre.replace("-",""))
                nombre_c=nombre_cs[1]
                pensum=pensums[1]
                nombre_c2=nombre_cs[0]
                pensum2=pensums[0]
                cursoglobal = Curso.objects.get(nombre=nombre_c)
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                cursoglobal2 = Curso.objects.get(nombre=nombre_c2)
                id_cursoglobal2 = cursoglobal2.id
                curso_asig2 = Curso_asignado.objects.get(id_curso=id_cursoglobal2,version_pensum=pensum2)
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
                        curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig2,semestre=semestre)
                        return HttpResponse("Ya hay un microcurriculo asignado en el semestre seleccionado")
                    except:
                        insert = Curso_programado(id_microcurriculos=microcurriculo,id_curso_asignado=curso_asig2,semestre=semestre)
                        insert.save()
                        return HttpResponse("Se asignó correctamente el ultimo microcurriculo vigente al semestre seleccionado")    
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
            elif(request.POST['caso']=="renovar2"):
                pensums = request.POST['pensum'].split(' /pencur- ')
                cursos = request.POST['curso'].split(' /cursel- ')
                pensum = pensums[0]
                nombre_c = cursos[0]
                vigencia = request.POST['vigencia']
                semestre = request.POST['semestre']
                cursoglobal = Curso.objects.get(nombre=nombre_c)
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                curso_asociados = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=vigencia[0:6])
                micro_aso = Microcurriculum.objects.get(id=curso_asociados.id_microcurriculos.id)
                cursoglobal = Curso.objects.get(nombre=cursos[1])
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensums[1])
                try:
                    curso_asociado2 = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=semestre)
                    return HttpResponse("Ya hay un microcurriculo asignado en el semestre seleccionado")
                except:
                    insert = Curso_programado(id_microcurriculos=micro_aso,id_curso_asignado=curso_asig,semestre=semestre)
                    insert.save()
                    return HttpResponse("Se renovó correctamente el microcurriculo del curso")        
            elif(request.POST['caso']=="nuevopdf"):
                pensum = request.POST['pensum']
                nombre_c = request.POST['curso']
                vigencia = request.POST['vigencia']
                cursoglobal=Curso.objects.get(nombre=nombre_c)
                #Datos extraidos de la base de datos curso
                codicur=cursoglobal.codigo
                nomcur=cursoglobal.nombre
                credicur=str(cursoglobal.num_creditos)
                #Datos extraidos de la base de datos curso asignado
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                hoteo=str(curso_asig.horas_t)
                hoteopr=str(curso_asig.horas_tp)
                hoprac=str(curso_asig.horas_p)
                if(curso_asig.validable==True):
                    valcur="Si"
                else:
                    valcur="No"
                if(curso_asig.habilitable==True):
                    habcur="Si"
                else:
                    habcur="No"
                if(curso_asig.clasificable==True):
                    clascur="Si"
                else:
                    clascur="No"        
                vigencur=vigencia
                semcur=str(curso_asig.nivel)
                #preguntar semanas donde esta
                semncur="16"
                areacur=curso_asig.area
                progrcur=curso_asig.id_programa.nombre_progr
                precur=curso_asig.prereq
                corrcur=curso_asig.correq
                #Datos extraidos de la base de datos microcurriculos
                curso_asociados = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=vigencia[0:6])
                micro_aso = Microcurriculum.objects.get(id=curso_asociados.id_microcurriculos.id)
                propcur=micro_aso.proposito
                propcur=propcur.replace('\n','\\\\')
                justificacion=micro_aso.descripcion_general
                justificacion=justificacion.replace('\n','\\\\')
                generales=micro_aso.objetivo_general
                objgeni=cadenas(generales," /objgen- ")
                especificos=micro_aso.objetivo_especifico
                objespi=cadenas(especificos," /objesp- ")
                items=micro_aso.contenido_resumido
                itemires=cadenas(items," /contresu- ")
                metodocur=micro_aso.metodologia
                metodocur=metodocur.replace('\n','\\\\')
                actiasiscur=micro_aso.actividades_asis_oblig
                actiasiscur=actiasiscur.replace('\n','\\\\')
                basicas=micro_aso.bibliografia_basica
                biblbasi=cadenas(basicas," /biblibas- ")
                complements=micro_aso.bibliografia_complementaria
                biblcompi=cadenas(complements," /biblicom- ")
                #Datos extraidos de las evaluaciones            
                evaluaciones=Evaluation.objects.filter(id_microcurriculos=micro_aso)
                actividadescuri=''
                for evaluacion in evaluaciones:
                    actividadescuri=actividadescuri+evaluacion.actividad+" & "+evaluacion.porcentaje+" & "+str(evaluacion.fecha)+" \\\\ "
                #Datos extraidos de las unidades
                unitys=Unity.objects.filter(id_microcurriculos=micro_aso)
                unidades=''
                cont=1
                for unit in unitys:
                    subt=unit.subtema
                    subtemas=cadenas(subt," /subin- ")
                    unidades=unidades+"\\begin{tabular}{R{0.16\\textwidth} L{0.7\\textwidth}} \n \\\\ \n\\toprule \\textbf{Unidad No. "+str(cont)+"} & "+unit.tema+" \n \\\\ \n\midrule\\textbf{Subtemas} & \n\\begin{description}\n "+subtemas+"\n\end{description}\n \\\\ \n\\textbf{Semanas} & "+str(unit.num_semanas)+" \n\end{tabular} \n \\\\ \n "
                    cont+=1    
                generate_pdf(codicur,nomcur,hoteo,hoteopr,hoprac,valcur,habcur,clascur,vigencur,semcur,semncur,areacur,credicur,progrcur,propcur,justificacion,precur,corrcur,objgeni,objespi,itemires,metodocur,actiasiscur,biblbasi,biblcompi,actividadescuri,unidades)
                with open("salida.pdf", "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
                    a=str(encoded_string)
                    a=a.replace("b'","")
                    a=a.replace("'","")
                return HttpResponse(a)
        semestres = Semestres.objects.all()
        return render(request, "core/curso.html",{'semestres':semestres})
    return redirect('/login')    

def asignar(request):
    if request.user.is_authenticated:
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
            elif(request.POST['caso']=="nuevopdf"):
                pensum = request.POST['version_p']
                nombre_c = request.POST['curso_es']
                vigencia = request.POST['semestre_es']
                cursoglobal=Curso.objects.get(nombre=nombre_c)
                #Datos extraidos de la base de datos curso
                codicur=cursoglobal.codigo
                nomcur=cursoglobal.nombre
                credicur=str(cursoglobal.num_creditos)
                #Datos extraidos de la base de datos curso asignado
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                hoteo=str(curso_asig.horas_t)
                hoteopr=str(curso_asig.horas_tp)
                hoprac=str(curso_asig.horas_p)
                if(curso_asig.validable==True):
                    valcur="Si"
                else:
                    valcur="No"
                if(curso_asig.habilitable==True):
                    habcur="Si"
                else:
                    habcur="No"
                if(curso_asig.clasificable==True):
                    clascur="Si"
                else:
                    clascur="No"        
                vigencur=vigencia
                semcur=str(curso_asig.nivel)
                #preguntar semanas donde esta
                semncur="16"
                areacur=curso_asig.area
                progrcur=curso_asig.id_programa.nombre_progr
                precur=curso_asig.prereq
                corrcur=curso_asig.correq
                #Datos extraidos de la base de datos microcurriculos
                pensum = request.POST['pensum']
                nombre_c = request.POST['curso']
                vigencia = request.POST['vigencia']
                cursoglobal=Curso.objects.get(nombre=nombre_c)
                id_cursoglobal = cursoglobal.id
                curso_asig = Curso_asignado.objects.get(id_curso=id_cursoglobal,version_pensum=pensum)
                curso_asociados = Curso_programado.objects.get(id_curso_asignado=curso_asig,semestre=vigencia[0:6])
                micro_aso = Microcurriculum.objects.get(id=curso_asociados.id_microcurriculos.id)
                propcur=micro_aso.proposito
                propcur=propcur.replace('\n','\\\\')
                justificacion=micro_aso.descripcion_general
                justificacion=justificacion.replace('\n','\\\\')
                generales=micro_aso.objetivo_general
                objgeni=cadenas(generales,"/objgen-")
                especificos=micro_aso.objetivo_especifico
                objespi=cadenas(especificos,"/objesp-")
                items=micro_aso.contenido_resumido
                itemires=cadenas(items,"/contresu-")
                metodocur=micro_aso.metodologia
                metodocur=metodocur.replace('\n','\\\\')
                actiasiscur=micro_aso.actividades_asis_oblig
                actiasiscur=actiasiscur.replace('\n','\\\\')
                basicas=micro_aso.bibliografia_basica
                biblbasi=cadenas(basicas,"/biblibas-")
                complements=micro_aso.bibliografia_complementaria
                biblcompi=cadenas(complements,"/biblicom-")
                #Datos extraidos de las evaluaciones            
                evaluaciones=Evaluation.objects.filter(id_microcurriculos=micro_aso)
                actividadescuri=''
                for evaluacion in evaluaciones:
                    actividadescuri=actividadescuri+evaluacion.actividad+" & "+evaluacion.porcentaje+" & "+str(evaluacion.fecha)+" \\\\ "
                #Datos extraidos de las unidades
                unitys=Unity.objects.filter(id_microcurriculos=micro_aso)
                unidades=''
                cont=1
                for unit in unitys:
                    subt=unit.subtema
                    subtemas=cadenas(subt,"/subin-")
                    unidades=unidades+"\\begin{tabular}{R{0.16\\textwidth} L{0.7\\textwidth}} \n \\\\ \n\\toprule \\textbf{Unidad No. "+str(cont)+"} & "+unit.tema+" \n \\\\ \n\midrule\\textbf{Subtemas} & \n\\begin{description}\n "+subtemas+"\n\end{description}\n \\\\ \n\\textbf{Semanas} & "+str(unit.num_semanas)+" \n\end{tabular} \n \\\\ \n "
                    cont+=1    
                generate_pdf(codicur,nomcur,hoteo,hoteopr,hoprac,valcur,habcur,clascur,vigencur,semcur,semncur,areacur,credicur,progrcur,propcur,justificacion,precur,corrcur,objgeni,objespi,itemires,metodocur,actiasiscur,biblbasi,biblcompi,actividadescuri,unidades)
                with open("salida.pdf", "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
                    a=str(encoded_string)
                    a=a.replace("b'","")
                    a=a.replace("'","")
                return HttpResponse(a)
        semestres = Semestres.objects.all()
        return render(request, "core/asignar.html",{'semestres':semestres})
    return redirect('/login')

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
        
def generate_pdf(codicur,nomcur,hoteo,hoteopr,hoprac,valcur,habcur,clascur,vigencur,semcur,semncur,areacur,credicur,progrcur,propcur,justificacion,precur,corrcur,objgeni,objespi,itemires,metodocur,actiasiscur,biblbasi,biblcompi,actividadescuri,unidades):
    template="/home/nicolas/CursoDjango/Microcurriculos/Microcurriculos_Udea/core/templatex.tex"
    with open(template,'r',encoding="ISO-8859-1") as f:
        archivo=f.read()
    archivo=archivo.replace('codicur',codicur)
    archivo=archivo.replace('nomcur',nomcur)
    archivo=archivo.replace('hoteo',hoteo)
    archivo=archivo.replace('hotepr',hoteopr)
    archivo=archivo.replace('hoprac',hoprac)
    archivo=archivo.replace('valcur',valcur)
    archivo=archivo.replace('habcur',habcur)
    archivo=archivo.replace('clascur',clascur)
    archivo=archivo.replace('semcur',semcur)
    archivo=archivo.replace('semncur',semncur)
    archivo=archivo.replace('areacur',areacur)
    archivo=archivo.replace('credicur',credicur)
    archivo=archivo.replace('progrcur',progrcur)
    archivo=archivo.replace('vigencur',vigencur)
    archivo=archivo.replace('justcur',justificacion)
    archivo=archivo.replace('precur',precur)
    archivo=archivo.replace('corrcur',corrcur)
    archivo=archivo.replace('propcur',propcur)
    archivo=archivo.replace('objgeni',objgeni)
    archivo=archivo.replace('objespi',objespi)
    archivo=archivo.replace('itemires',itemires)
    archivo=archivo.replace('metodocur',metodocur)
    archivo=archivo.replace('actiasiscur',actiasiscur)
    archivo=archivo.replace('biblbasi',biblbasi)
    archivo=archivo.replace('biblcompi',biblcompi)
    archivo=archivo.replace('actividadescuri',actividadescuri)
    archivo=archivo.replace('unidcuri',unidades)
    with open ("salida.tex",'w') as h:
        h.write(archivo)
    d=os.getcwd()
    call("pdflatex "+d+"/salida.tex",shell=1)        

def cadenas(iniciales,clave):
    salida=''
    iniciales=iniciales.split(clave)
    for inicial in iniciales:
        if(inicial!=''):
            inicial=inicial.replace('&','\&')
            salida=salida+'\item '+inicial+' '
    return salida                     

def procesos(cadena1,request):
    cadena2=request.POST[cadena1]
    cadena2=cadena2.replace('\n','\\\\')
    cadena2=cadena2.replace('&','\&')
    return cadena2