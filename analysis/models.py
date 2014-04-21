from django.db import models
from djorm_pgarray.fields import ArrayField


class MusicXMLScore(models.Model):
    filename = models.CharField(max_length=300)
    score_id = models.CharField(max_length=300)
    score = models.TextField()


class MusicData(models.Model):
    musicXML_score = models.ForeignKey(MusicXMLScore)

    notes_midi = ArrayField(dbtype="int")
    # notes are represented in base40
    notes = ArrayField(dbtype="int")
    intervals = ArrayField(dbtype="int")
    intervals_with_direction = ArrayField(dbtype="int")
    durations = ArrayField(dbtype="float")
    contour = ArrayField(dbtype="int")

    mode = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    time_signature = models.CharField(max_length=100)
    # we get it with quarterLength
    total_duration = models.FloatField()
    # as a MIDI interval
    ambitus = models.IntegerField()


class Composer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_birth = models.DateField()
    date_death = models.DateField()
    place_birth = models.CharField(max_length=200)
    place_death = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    time_period = models.CharField(max_length=200)


class CompositionType(models.Model):
    """Things like Symphony, Etude, etc"""
    name = models.CharField(max_length=200)


class Composition(models.Model):
    music_data = models.ForeignKey(MusicData)

    composer = models.ForeignKey(Composer)
    composition_type = models.ForeignKey(CompositionType)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)

    editor = models.CharField(max_length=200)
    publisher_information = models.CharField(max_length=200)
    misc_notes = models.CharField(max_length=200)
    description = models.TextField()
    uploader = models.CharField(max_length=200)
    pagecount = models.IntegerField()
    raw_pagecount = models.IntegerField()
    rating = models.IntegerField()


class Collection(models.Model):
    imslp_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    compositions = models.ForeignKey(Composition)
