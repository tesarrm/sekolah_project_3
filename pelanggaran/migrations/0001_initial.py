# Generated by Django 5.0.6 on 2024-05-18 00:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('akademik', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PelanggaranKategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('poin', models.IntegerField()),
                ('catatan', models.TextField()),
                ('sekolah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.sekolah')),
            ],
        ),
        migrations.CreateModel(
            name='Pelanggaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pesan', models.TextField()),
                ('sekolah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.sekolah')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.siswa')),
                ('staff_sekolah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.staffsekolah')),
                ('pelanggaran_kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pelanggaran.pelanggarankategori')),
            ],
        ),
    ]
