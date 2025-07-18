from django.db import models

class Estado(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    capital = models.BooleanField(
        verbose_name="É capital?",
        choices=[(True, "Sim"), (False, "Não")],
        default=False
    )
    mais_de_80_mil_hab = models.BooleanField(
        verbose_name="Tem mais de 80 mil habitantes?",
        choices=[(True, "Sim"), (False, "Não")],
        default=False
    )
    regiao_metropolitana = models.BooleanField(
        verbose_name="Pertence à região metropolitana?",
        choices=[(True, "Sim"), (False, "Não")],
        default=False
    )
    nome_metropolitana = models.CharField(max_length=100, null=True)
    nome_regiao = models.CharField(max_length=100)

    adimplente = models.BooleanField(
        default=False,
        verbose_name="Município Adimplente"
    )

    def __str__(self):
        return f"{self.nome} - {self.estado.nome}"


class Interesse(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Partido(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Cargo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)  # nunca nulo
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    observacoes = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    foto_url = models.URLField(max_length=300, blank=True, null=True)
    interesses = models.ManyToManyField('Interesse', blank=True)
    entidade = models.CharField(max_length=100, blank=True)
    partido = models.ForeignKey(Partido, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"


class Email(models.Model):
    contact = models.ForeignKey(Contato, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email


class Telephone(models.Model):
    contact = models.ForeignKey(Contato, related_name='telephones', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.telephone
