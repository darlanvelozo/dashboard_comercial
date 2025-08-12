from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LeadProspecto, Prospecto


@receiver(post_save, sender=LeadProspecto)
def relate_prospecto_when_lead_has_hubsoft(sender, instance: LeadProspecto, created, **kwargs):
    """Quando um LeadProspecto com id_hubsoft é salvo, vincula Prospecto que
    tenha o mesmo id_prospecto_hubsoft automaticamente.
    """
    id_hub = (instance.id_hubsoft or '').strip()
    if not id_hub:
        return

    # Atualiza o Prospecto que tenha o mesmo id no Hubsoft para apontar este lead
    Prospecto.objects.filter(id_prospecto_hubsoft=id_hub).exclude(lead=instance).update(lead=instance)


@receiver(post_save, sender=Prospecto)
def relate_lead_when_prospecto_has_hubsoft(sender, instance: Prospecto, created, **kwargs):
    """Quando um Prospecto com id_prospecto_hubsoft é salvo e não tem lead,
    tenta relacionar com LeadProspecto cujo id_hubsoft seja igual.
    """
    if instance.lead_id:
        return

    id_hub = (instance.id_prospecto_hubsoft or '').strip()
    if not id_hub:
        return

    lead = LeadProspecto.objects.filter(id_hubsoft=id_hub).first()
    if lead:
        # Evita recursão de signals usando update direto no queryset
        Prospecto.objects.filter(pk=instance.pk, lead__isnull=True).update(lead=lead)
