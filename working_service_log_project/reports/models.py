from django.db import models


class EquipmentModel(models.Model):
    name = models.CharField("Модель техники",max_length=100)

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField("Название организации", max_length=255)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT, verbose_name="Модель",null=True, blank=True)
    factory_number = models.CharField("Заводской номер", max_length=50, unique=True)
    garage_number = models.CharField("Гаражный номер", max_length=50, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name="Предприятяие",null=True, blank=True)
    warranty = models.BooleanField("Гарантия", default=False)

    def __str__(self):
        return f"{self.factory_number} / {self.garage_number}"

class Personal(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=255)
    tab_number = models.CharField("Табельный №", max_length=50, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name="Предприятие",null=True, blank=True)

    def __str__(self):
        return self.full_name


class Reglament(models.Model):
    name = models.CharField("Вид регламентного ТО", max_length=10)

    def __str__(self):
        return self.name

class ServiceReport(models.Model):
    equip_model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT, verbose_name="Модель",null=True, blank=True)
    service_act_number = models.CharField("Номер АВР", max_length=10,null=True, blank=True)
    service_request_number = models.CharField("Номер заявки", max_length=10,null=True, blank=True)
    service_organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name="Предприятие")
    service_work_place = models.CharField("Отметка", max_length=50,null=True, blank=True)
    service_manager_fio = models.CharField("ФИО ответсвенного за выполнение работ", max_length=255)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, verbose_name="Оборудование (зав.№/гар.№)")
    equip_current_narabotka = models.CharField("Текущая наработка, м/ч", max_length=10)
    service_work_date = models.DateField("Дата выполнения работ")
    service_time_start = models.TimeField("Время начала работ")
    service_time_end = models.TimeField("Время окончания работ")
    service_work_duration = models.CharField("Длительность работ", max_length=10)
    service_reglament_work_type = models.ForeignKey(Reglament, on_delete=models.PROTECT, verbose_name="Вид регламентного обслуживания",null=True, blank=True)
    service_work_description = models.TextField("Выполненные дополнительные работы")
    service_used_materials = models.TextField("Использованные запасные части и материалы")
    service_defect_description = models.TextField("Выявленные отклонения/коды ошибок")
    service_recomendation = models.TextField("Рекомендации")
    service_customer_fio = models.CharField("ФИО заказчика", max_length=255)
    service_employer_fio = models.ManyToManyField('Personal',verbose_name="Исполнители работ")
    service_pdf_file = models.FileField("PDF файл акта выполненных работ", upload_to='pdfs/',null=True, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"Акт №{self.service_act_number} от {self.service_work_date}"
