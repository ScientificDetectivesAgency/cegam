from django.contrib.gis.db import models


class ConservacionManglares(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    ha = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos"."conservacion_manglares'


class CrestasArrecifales(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    nom_clase = models.CharField(max_length=255, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos"."crestas_arrecifales'


class PuntoCosta(models.Model):
    nombre = models.CharField(max_length=200, help_text="Nombre del punto o ubicación")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción o detalles relevantes")
    geom = models.PointField(srid=4326, help_text="Coordenadas exactas en la línea de costa")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Punto de Costa"
        verbose_name_plural = "Puntos de Costa"

class FotoPunto(models.Model):
    punto = models.ForeignKey(PuntoCosta, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='fotos_costa/')
    leyenda = models.CharField(max_length=255, blank=True, null=True, help_text="Pie de foto opcional")
    subida_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.punto.nombre}"

class DatosPlayas(models.Model):
    id = models.CharField(primary_key=True)
    nombre_tramo = models.CharField(blank=True, null=True)
    coord_init = models.CharField(blank=True, null=True)
    coord_final = models.CharField(blank=True, null=True)
    long = models.CharField(blank=True, null=True)
    tipo_geomorfo = models.CharField(blank=True, null=True)
    subtipo_detallado = models.CharField(blank=True, null=True)
    tipo_playa = models.CharField(blank=True, null=True)
    nivel_energia = models.CharField(blank=True, null=True)
    dir_dominante = models.CharField(blank=True, null=True)
    mag_estimada = models.CharField(blank=True, null=True)
    fuentes_sedimento = models.CharField(blank=True, null=True)
    sumideros_sedimento = models.CharField(blank=True, null=True)
    balance_sedimentario = models.CharField(blank=True, null=True)
    est_costeras = models.CharField(blank=True, null=True)
    ev_erosion = models.CharField(blank=True, null=True)
    influ_arrecifal = models.CharField(blank=True, null=True)
    influ_manglar = models.CharField(blank=True, null=True)
    pres_antropic = models.CharField(blank=True, null=True)
    conectividad = models.CharField(blank=True, null=True)
    incertidumbre = models.CharField(blank=True, null=True)
    tipo_soporte = models.CharField(blank=True, null=True)
    geom_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos_playas'


class TcQrN3(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiLineStringField(srid=4326)
    
    # Campos mapeados con db_column a la nueva tabla datos.tc_qr_n3_v2
    name = models.CharField(db_column='nom_trm', max_length=255, blank=True, null=True)
    cod_name = models.CharField(db_column='cod_trm', max_length=255, blank=True, null=True)
    longitud = models.FloatField(db_column='long_km', blank=True, null=True)
    t_geomo = models.CharField(db_column='tipo_geo', max_length=255, blank=True, null=True)
    subtipo = models.CharField(db_column='sub_tipo', max_length=255, blank=True, null=True)
    t_playa = models.CharField(db_column='tipo_ply', max_length=255, blank=True, null=True)
    n_energi = models.CharField(db_column='nivel_e', max_length=255, blank=True, null=True)
    d_t_lito = models.CharField(db_column='dir_tr', max_length=255, blank=True, null=True)
    magn_m3a = models.CharField(db_column='mag_tr', max_length=255, blank=True, null=True)
    fuentsed = models.CharField(db_column='ft_sed', max_length=255, blank=True, null=True)
    sumidero = models.CharField(db_column='sm_sed', max_length=255, blank=True, null=True)
    bal_m3a = models.CharField(db_column='bal_sed', max_length=255, blank=True, null=True)
    est_cost = models.CharField(db_column='est_csv', max_length=255, blank=True, null=True)
    eros_acr = models.CharField(db_column='tasa_er', max_length=255, blank=True, null=True)
    inf_arre = models.CharField(db_column='inf_sam', max_length=255, blank=True, null=True)
    inf_mang = models.CharField(db_column='inf_mgl', max_length=255, blank=True, null=True)
    p_antrop = models.CharField(db_column='pres_ant', max_length=255, blank=True, null=True)
    conectiv = models.CharField(db_column='con_sed', max_length=255, blank=True, null=True)
    incertid = models.CharField(db_column='incert', max_length=255, blank=True, null=True)
    evidenci = models.CharField(db_column='evidnc', max_length=255, blank=True, null=True)
    municip = models.CharField(db_column='mpios', max_length=255, blank=True, null=True)
    anps = models.CharField(db_column='anps', max_length=255, blank=True, null=True)
    
    # Coordenadas mapeadas
    y_inicio = models.FloatField(db_column='lat_ini', blank=True, null=True)
    x_inicio = models.FloatField(db_column='lon_ini', blank=True, null=True)
    y_fin = models.FloatField(db_column='lat_fin', blank=True, null=True)
    x_fin = models.FloatField(db_column='lon_fin', blank=True, null=True)

    # Nuevos campos de la tabla v2
    cal_agua = models.CharField(max_length=255, blank=True, null=True)
    d15n = models.CharField(max_length=255, blank=True, null=True)
    est_dun = models.CharField(max_length=255, blank=True, null=True)
    est_pmr = models.CharField(max_length=255, blank=True, null=True)
    est_mgl = models.CharField(max_length=255, blank=True, null=True)
    hs_m = models.FloatField(blank=True, null=True)
    g_antrop = models.CharField(max_length=255, blank=True, null=True)
    en_mar = models.CharField(max_length=255, blank=True, null=True)
    hsb_m = models.CharField(max_length=255, blank=True, null=True)
    alpha_b = models.CharField(max_length=255, blank=True, null=True)
    sent_net = models.CharField(max_length=255, blank=True, null=True)
    ql_m3yr = models.CharField(max_length=255, blank=True, null=True)

    # Propiedades calculadas para mantener compatibilidad sin que Django las pida en el SELECT
    @property
    def fid(self):
        return self.id

    @property
    def celda(self):
        if self.cod_name:
            parts = self.cod_name.split('-')
            if len(parts) >= 2:
                return '-'.join(parts[:2])
        return "N/A"

    @property
    def subcelda(self):
        if self.cod_name:
            parts = self.cod_name.split('-')
            if len(parts) >= 3:
                return parts[2]
        return "N/A"

    @property
    def tipo(self):
        return self.t_geomo

    @property
    def ac_calle(self):
        return "No disponible"

    @property
    def c_eros(self):
        return "No disponible"

    @property
    def protcons(self):
        return "No disponible"

    @property
    def aprovsos(self):
        return "No disponible"

    @property
    def infcost(self):
        return "No disponible"

    @property
    def gesries(self):
        return "No disponible"

    @property
    def gobgest(self):
        return "No disponible"

    class Meta:
        managed = False
        db_table = 'datos"."tc_qr_n3_v2'


class CelQrN1(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    n_sub = models.CharField(max_length=255, blank=True, null=True)
    n_tramo = models.CharField(max_length=255, blank=True, null=True)
    lon_km = models.CharField(max_length=255, blank=True, null=True)
    subceldas = models.CharField(max_length=255, blank=True, null=True)
    tramos = models.CharField(max_length=255, blank=True, null=True)
    sistema = models.CharField(max_length=255, blank=True, null=True)
    procesos = models.CharField(max_length=255, blank=True, null=True)
    arrecife = models.CharField(max_length=255, blank=True, null=True)
    manglar = models.CharField(max_length=255, blank=True, null=True)
    asuprinc = models.CharField(max_length=255, blank=True, null=True)
    estconsv = models.CharField(max_length=255, blank=True, null=True)
    t_geomos = models.CharField(max_length=255, blank=True, null=True)
    municip = models.CharField(max_length=255, blank=True, null=True)
    anps = models.CharField(max_length=255, blank=True, null=True)
    c_eros = models.CharField(max_length=255, blank=True, null=True)
    protcons = models.CharField(max_length=255, blank=True, null=True)
    aprovsos = models.CharField(max_length=255, blank=True, null=True)
    infcost = models.CharField(max_length=255, blank=True, null=True)
    gesries = models.CharField(max_length=255, blank=True, null=True)
    gobgest = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos"."cel_qr_n1'


class SubcelQrN2(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    celda = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nomcelda = models.CharField(max_length=255, blank=True, null=True)
    n_tramo = models.CharField(max_length=255, blank=True, null=True)
    lon_km = models.CharField(max_length=255, blank=True, null=True)
    tramos = models.CharField(max_length=255, blank=True, null=True)
    arquetip = models.CharField(max_length=255, blank=True, null=True)
    caracter = models.CharField(max_length=255, blank=True, null=True)
    t_geomos = models.CharField(max_length=255, blank=True, null=True)
    municip = models.CharField(max_length=255, blank=True, null=True)
    anps = models.CharField(max_length=255, blank=True, null=True)
    c_eros = models.CharField(max_length=255, blank=True, null=True)
    protcons = models.CharField(max_length=255, blank=True, null=True)
    aprovsos = models.CharField(max_length=255, blank=True, null=True)
    infcost = models.CharField(max_length=255, blank=True, null=True)
    gesries = models.CharField(max_length=255, blank=True, null=True)
    gobgest = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos"."subcel_qr_n2'
