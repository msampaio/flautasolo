# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MusicData.intervals_classes'
        db.add_column('analysis_musicdata', 'intervals_classes',
                      self.gf('djorm_pgarray.fields.ArrayField')(default=None, blank=True, dbtype='varchar', null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MusicData.intervals_classes'
        db.delete_column('analysis_musicdata', 'intervals_classes')


    models = {
        'analysis.collection': {
            'Meta': {'object_name': 'Collection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composer': {
            'Meta': {'object_name': 'Composer'},
            'date_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'date_death': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nationality': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'place_birth': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'place_death': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composition': {
            'Meta': {'object_name': 'Composition'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Collection']"}),
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Composer']"}),
            'composition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.CompositionType']", 'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'misc_notes': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'music_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MusicData']"}),
            'pagecount': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publisher_information': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'raw_pagecount': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.compositiontype': {
            'Meta': {'object_name': 'CompositionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.musicdata': {
            'Meta': {'object_name': 'MusicData'},
            'ambitus': ('django.db.models.fields.IntegerField', [], {}),
            'contour': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'durations': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'dbtype': "'float'", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervals': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'dbtype': "'varchar'", 'null': 'True'}),
            'intervals_classes': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'dbtype': "'varchar'", 'null': 'True'}),
            'intervals_midi': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'intervals_with_direction': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'dbtype': "'varchar'", 'null': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'key_midi': ('django.db.models.fields.IntegerField', [], {}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'notes_midi': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MusicXMLScore']"}),
            'time_signature': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_duration': ('django.db.models.fields.FloatField', [], {})
        },
        'analysis.musicxmlscore': {
            'Meta': {'object_name': 'MusicXMLScore'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['analysis']