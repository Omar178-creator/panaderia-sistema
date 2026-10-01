from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from cuentas.models import Usuario
from personal.models import MarcadoAsistencia, AvisoFalta


class Command(BaseCommand):
    help = 'Marca como falta a los trabajadores que no marcaron llegada después de 3 horas de tolerancia'

    def handle(self, *args, **kwargs):
        ahora = timezone.now()
        hoy = ahora.date()

        for trabajador in Usuario.objects.filter(horario_entrada__isnull=False):
            ya_marco = MarcadoAsistencia.objects.filter(trabajador=trabajador, fecha=hoy).exists()
            if ya_marco:
                continue

            hora_esperada = datetime.combine(hoy, trabajador.horario_entrada, tzinfo=ahora.tzinfo)
            if ahora - hora_esperada >= timedelta(hours=3):
                aviso = AvisoFalta.objects.filter(trabajador=trabajador, fecha_falta=hoy).first()
                estado = 'falta_avisada' if aviso else 'falta_sin_aviso'

                MarcadoAsistencia.objects.create(
                    trabajador=trabajador,
                    fecha=hoy,
                    estado=estado,
                    hora_marcado=None
                )
                self.stdout.write(f"Falta registrada: {trabajador} ({estado})")