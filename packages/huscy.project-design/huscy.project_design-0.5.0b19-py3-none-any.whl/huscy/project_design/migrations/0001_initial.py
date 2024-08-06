import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAcquisitionMethodType',
            fields=[
                ('short_name', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, verbose_name='Short name')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Data acquisition method type',
                'verbose_name_plural': 'Data acquisition method types',
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Experiment',
                'verbose_name_plural': 'Experiments',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('contacts', models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='project_design.experiment', verbose_name='Experiment')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='DataAcquisitionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('setup_time', models.DurationField(default=datetime.timedelta(0), verbose_name='Setup time')),
                ('duration', models.DurationField(verbose_name='Duration')),
                ('teardown_time', models.DurationField(default=datetime.timedelta(0), verbose_name='Teardown time')),
                ('stimulus', models.CharField(choices=[('auditive', 'Auditive'), ('gustatory', 'Gustatory'), ('haptic', 'Haptic'), ('olfactory', 'Olfactory'), ('visual', 'Visual')], max_length=32, null=True, verbose_name='Stimulus')),
                ('location', models.CharField(max_length=126, verbose_name='Location')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project_design.dataacquisitionmethodtype', verbose_name='Type')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_acquisition_methods', to='project_design.session', verbose_name='Session')),
            ],
            options={
                'verbose_name': 'Data acquisition method',
                'verbose_name_plural': 'Data acquisition methods',
            },
        ),
    ]
