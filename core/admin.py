from django.contrib import admin
from .models import Microcurriculum,Unity,Evaluation,Curso,Programa,Curso_asignado,Curso_programado,Semestres,Microcurriculum_2,Unity_2,Evaluation_2,Solicitud

# Register your models here.
class MicrocurriculumAdmin(admin.ModelAdmin):
    list_display = ('id','descripcion_general','proposito','objetivo_general','objetivo_especifico','contenido_resumido','actividades_asis_oblig','bibliografia_basica','bibliografia_complementaria','metodologia')

class Microcurriculum2Admin(admin.ModelAdmin):
    list_display = ('id','descripcion_general','proposito','objetivo_general','objetivo_especifico','contenido_resumido','actividades_asis_oblig','bibliografia_basica','bibliografia_complementaria','metodologia')

class UnityAdmin(admin.ModelAdmin):
    list_display = ('id','id_microcurriculos','tema','subtema','num_semanas')

class Unity2Admin(admin.ModelAdmin):
    list_display = ('id','id_microcurriculos','tema','subtema','num_semanas')

class Evaluation2Admin(admin.ModelAdmin):
    list_display = ('id','id_microcurriculos','actividad','porcentaje','fecha')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id','soli','descripcion','curso_destino','pensum_destino','curso_propietario','pensum_propietario','semestre_asignar','microcurriculo','usuario')

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id','id_microcurriculos','actividad','porcentaje','fecha')

class CursoAdmin(admin.ModelAdmin):
    list_display = ('id','codigo','nombre','num_creditos')

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_progr')

class Curso_asignadoAdmin(admin.ModelAdmin):
    list_display = ('id','id_programa','id_curso','nivel','version_pensum','area','horas_t','horas_p','horas_tp','horas_especiales','habilitable','validable','clasificable','prereq','correq')

class Curso_programadoAdmin(admin.ModelAdmin):
    list_display = ('id','id_microcurriculos','id_curso_asignado','semestre')

class SemestresAdmin(admin.ModelAdmin):
    list_display = ('id','descripcion')

admin.site.register(Microcurriculum,MicrocurriculumAdmin)
admin.site.register(Microcurriculum_2,Microcurriculum2Admin)
admin.site.register(Unity,UnityAdmin)
admin.site.register(Unity_2,Unity2Admin)
admin.site.register(Evaluation,EvaluationAdmin)
admin.site.register(Evaluation_2,Evaluation2Admin)
admin.site.register(Curso,CursoAdmin)
admin.site.register(Programa,ProgramaAdmin)
admin.site.register(Curso_asignado,Curso_asignadoAdmin)
admin.site.register(Curso_programado,Curso_programadoAdmin)
admin.site.register(Semestres,SemestresAdmin)
admin.site.register(Solicitud,SolicitudAdmin)