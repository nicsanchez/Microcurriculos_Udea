from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Base de datos para el administrador 
class Microcurriculum(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion_general = models.TextField(verbose_name="Descripcion General")
    proposito = models.TextField(verbose_name="Propósito")
    objetivo_general = models.TextField(verbose_name="Objetivo General")
    objetivo_especifico = models.TextField(verbose_name="Objetivo Especifico")
    contenido_resumido = models.TextField(verbose_name="Contenido Resumido")
    actividades_asis_oblig = models.CharField(max_length=255,verbose_name="Actividades de Asistencia Obligatoria")
    bibliografia_basica = models.TextField(verbose_name="Bibliografia Basica")
    bibliografia_complementaria = models.TextField(verbose_name="Bibliografía Complementaria")
    metodologia = models.TextField(verbose_name="Metodologia")

    class Meta:
        verbose_name = "Microcurriculo"
        verbose_name_plural = "Microcurriculos"
        ordering = ["id"]
    
    def __str__(self):
        return str(self.id)

class Unity(models.Model):
    id = models.AutoField(primary_key=True)
    id_microcurriculos = models.ForeignKey(Microcurriculum,verbose_name="Microcurriculo",on_delete=models.PROTECT)
    tema = models.CharField(max_length=255, verbose_name="Tema")
    subtema = models.TextField(verbose_name="Subtema")
    num_semanas = models.SmallIntegerField(verbose_name="Numero de semanas")
    
    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ["id"]

    def __str__(self):
        return str(self.id)

class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    id_microcurriculos = models.ForeignKey(Microcurriculum,verbose_name="Microcurriculo",on_delete=models.PROTECT)
    actividad = models.CharField(max_length=255, verbose_name="Actividad")
    porcentaje = models.CharField(max_length=255, verbose_name="Porcentaje")
    fecha = models.DateField(auto_now=False,auto_now_add=False,verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Evaluacion"
        verbose_name_plural = "Evaluaciones"
        ordering = ["id"]
        
    def __str__(self):
        return str(self.id)

#Base de datos para el administrador Editor
class Microcurriculum_2(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion_general = models.TextField(verbose_name="Descripcion General")
    proposito = models.TextField(verbose_name="Propósito")
    objetivo_general = models.TextField(verbose_name="Objetivo General")
    objetivo_especifico = models.TextField(verbose_name="Objetivo Especifico")
    contenido_resumido = models.TextField(verbose_name="Contenido Resumido")
    actividades_asis_oblig = models.CharField(max_length=255,verbose_name="Actividades de Asistencia Obligatoria")
    bibliografia_basica = models.TextField(verbose_name="Bibliografia Basica")
    bibliografia_complementaria = models.TextField(verbose_name="Bibliografía Complementaria")
    metodologia = models.TextField(verbose_name="Metodologia")

    class Meta:
        verbose_name = "Microcurriculo"
        verbose_name_plural = "Microcurriculos Editor"
        ordering = ["id"]
    
    def __str__(self):
        return str(self.id)

class Unity_2(models.Model):
    id = models.AutoField(primary_key=True)
    id_microcurriculos = models.ForeignKey(Microcurriculum_2,verbose_name="Microcurriculo",on_delete=models.PROTECT)
    tema = models.CharField(max_length=255, verbose_name="Tema")
    subtema = models.TextField(verbose_name="Subtema")
    num_semanas = models.SmallIntegerField(verbose_name="Numero de semanas")
    
    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades Editor"
        ordering = ["id"]

    def __str__(self):
        return str(self.id)

class Evaluation_2(models.Model):
    id = models.AutoField(primary_key=True)
    id_microcurriculos = models.ForeignKey(Microcurriculum_2,verbose_name="Microcurriculo",on_delete=models.PROTECT)
    actividad = models.CharField(max_length=255, verbose_name="Actividad")
    porcentaje = models.CharField(max_length=255, verbose_name="Porcentaje")
    fecha = models.DateField(auto_now=False,auto_now_add=False,verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Evaluacion"
        verbose_name_plural = "Evaluaciones Editor"
        ordering = ["id"]
        
    def __str__(self):
        return str(self.id)

#Base de datos para las solicitudes de los usuarios tipo Editor
class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    soli = models.CharField(max_length=255, verbose_name="Solicitud")
    estado = models.CharField(max_length=255, verbose_name="Estado")
    descripcion = models.TextField(verbose_name="Descripcion")
    curso_destino = models.CharField(max_length=255, verbose_name="Curso Destino")
    pensum_destino = models.CharField(max_length=255, verbose_name="Pensum Destino")
    curso_propietario = models.CharField(max_length=255, verbose_name="Curso Propietario")
    pensum_propietario = models.CharField(max_length=255, verbose_name="Pensum Propietario")
    semestre_asignar = models.CharField(max_length=255, verbose_name="Semestre a asignar")
    vigencias_original = models.CharField(max_length=255, verbose_name="Vigencia Original",null=True)
    microcurriculo = models.ForeignKey(Microcurriculum_2,verbose_name="Microcurriculo",on_delete=models.SET_NULL,null=True)
    archivo = models.FileField(upload_to="files/",verbose_name="Comentarios")
    usuario = models.CharField(max_length=255, verbose_name="Usuario que realizo la peticion")
    coordinador = models.CharField(max_length=255, verbose_name="Coordinador que estudio la peticion")
    original = models.CharField(max_length=255, verbose_name="Microcurriculo Original")
    tipo = models.CharField(max_length=255, verbose_name="Tipo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ["id"]

    def __str__(self):
        return str(self.id)


class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255, verbose_name="Codigo")
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    num_creditos = models.SmallIntegerField(verbose_name="Numero de Creditos")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["id"]

    def __str__(self):
        return (self.nombre)

class Programa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_progr = models.CharField(max_length=255, verbose_name="Nombre del programa")

    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
        ordering = ["id"]

    def __str__(self):
        return (self.nombre_progr)

class Curso_asignado(models.Model):
    id = models.AutoField(primary_key=True)
    id_programa = models.ForeignKey(Programa,verbose_name="Programa",on_delete=models.PROTECT)
    id_curso = models.ForeignKey(Curso,verbose_name="Curso",on_delete=models.PROTECT)
    nivel = models.SmallIntegerField(verbose_name="Nivel")
    version_pensum = models.SmallIntegerField(verbose_name="Version del Pensum")
    area = models.CharField(max_length=255, verbose_name="Area")
    horas_t = models.SmallIntegerField(verbose_name="Horas Teoricas")
    horas_p = models.SmallIntegerField(verbose_name="Horas Practicas")
    horas_tp = models.SmallIntegerField(verbose_name="Horas Teorico-Practica")
    horas_especiales = models.SmallIntegerField(verbose_name="Horas Especiales")
    habilitable = models.BooleanField(verbose_name="Habilitable")
    validable = models.BooleanField(verbose_name="Validable")
    clasificable = models.BooleanField(verbose_name="Clasificable")
    prereq = models.CharField(max_length=255,verbose_name="Prerrequisitos")
    correq = models.CharField(max_length=255,verbose_name="Corequisitos")

    class Meta:
        verbose_name = "Curso Asignado"
        verbose_name_plural = "Cursos Asignados"
        ordering = ["id"]

    def __str__(self):
        return self.id_curso.nombre

class Curso_programado(models.Model):
    id = models.AutoField(primary_key=True)
    id_microcurriculos = models.ForeignKey(Microcurriculum,verbose_name="Microcurriculo",on_delete=models.PROTECT)
    id_curso_asignado = models.ForeignKey(Curso_asignado,verbose_name="Curso Asignado",on_delete=models.PROTECT)
    semestre = models.CharField(max_length=255, verbose_name="Semestre")

    class Meta:
        verbose_name = "Curso Programado"
        verbose_name_plural = "Cursos Programados"
        ordering = ["id_microcurriculos"]

    def __str__(self):
        return str(self.id)

class Semestres(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name="Descripcion")
    
    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ["id"]
    
    def __str__(self):
        return str(self.descripcion)    

class Versiones(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.FileField(upload_to="versions/",verbose_name="Versiones")
    id_microcurriculos = models.ForeignKey(Microcurriculum,verbose_name="Microcurriculo final",on_delete=models.PROTECT,null=True)
    id_microcurriculos_2 = models.ForeignKey(Microcurriculum_2,verbose_name="Microcurriculo fantasma",on_delete=models.SET_NULL,null=True)
    accion = models.CharField(max_length=255, verbose_name="Accion")
    comentarios = models.FileField(upload_to="files/",verbose_name="Comentarios",null=True)
    usuario = models.CharField(max_length=255, verbose_name="Usuario que realizo la peticion")
    coordinador = models.CharField(max_length=255, verbose_name="Coordinador que analizo la peticion")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")
    
    class Meta:
        verbose_name = "Version"
        verbose_name_plural = "Versiones"
        ordering = ["id"]
    
    def __str__(self):
        return str(self.id)

class UserRol(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    departamento = models.ForeignKey(Programa, on_delete=models.PROTECT,null=True)
    rol = models.TextField(null=True)
    cursos = models.ManyToManyField(Curso_asignado,verbose_name="Cursos")

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
        ordering = ["id"]
    
    def __str__(self):
        return str(self.rol)