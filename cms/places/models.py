from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.models import *
import datetime
from cms.categories.models import Category


class PlaceType(Category):

	class Meta:
		verbose_name = 'place type'
		verbose_name_plural = 'place types'

	def __unicode__(self):
		return '%s' % self.title

class City(models.Model):
	COUNTRY_CHOICES = (("AF", "Afghanistan"),("AX", "Aland Islands"),("AL", "Albania"),("DZ", "Algeria"),("AS", "American Samoa"),("AD", "Andorra"),("AO", "Angola"),("AI", "Anguilla"),("AQ", "Antarctica"),("AG", "Antigua and Barbuda"),("AR", "Argentina"),("AM", "Armenia"),("AW", "Aruba"),("AU", "Australia"),("AT", "Austria"),("AZ", "Azerbaijan"),("BS", "Bahamas"),("BH", "Bahrain"),("BD", "Bangladesh"),("BB", "Barbados"),("BY", "Belarus"),("BE", "Belgium"),("BZ", "Belize"),("BJ", "Benin"),("BM", "Bermuda"),("BT", "Bhutan"),("BO", "Bolivia, Plurinational State of"),("BQ", "Bonaire, Saint Eustatius and Saba"),("BA", "Bosnia and Herzegovina"),("BW", "Botswana"),("BV", "Bouvet Island"),("BR", "Brazil"),("IO", "British Indian Ocean Territory"),("BN", "Brunei Darussalam"),("BG", "Bulgaria"),("BF", "Burkina Faso"),("BI", "Burundi"),("KH", "Cambodia"),("CM", "Cameroon"),("CA", "Canada"),("CV", "Cape Verde"),("KY", "Cayman Islands"),("CF", "Central African Republic"),("TD", "Chad"),("CL", "Chile"),("CN", "China"),("CX", "Christmas Island"),("CC", "Cocos (Keeling) Islands"),("CO", "Colombia"),("KM", "Comoros"),("CG", "Congo"),("CD", "Congo, The Democratic Republic of the"),("CK", "Cook Islands"),("CR", "Costa Rica"),("CI", "Cote D'ivoire"),("HR", "Croatia"),("CU", "Cuba"),("CW", "Curacao"),("CY", "Cyprus"),("CZ", "Czech Republic"),("DK", "Denmark"),("DJ", "Djibouti"),("DM", "Dominica"),("DO", "Dominican Republic"),("EC", "Ecuador"),("EG", "Egypt"),("SV", "El Salvador"),("GQ", "Equatorial Guinea"),("ER", "Eritrea"),("EE", "Estonia"),("ET", "Ethiopia"),("FK", "Falkland Islands (Malvinas)"),("FO", "Faroe Islands"),("FJ", "Fiji"),("FI", "Finland"),("FR", "France"),("GF", "French Guiana"),("PF", "French Polynesia"),("TF", "French Southern Territories"),("GA", "Gabon"),("GM", "Gambia"),("GE", "Georgia"),("DE", "Germany"),("GH", "Ghana"),("GI", "Gibraltar"),("GR", "Greece"),("GL", "Greenland"),("GD", "Grenada"),("GP", "Guadeloupe"),("GU", "Guam"),("GT", "Guatemala"),("GG", "Guernsey"),("GN", "Guinea"),("GW", "Guinea-Bissau"),("GY", "Guyana"),("HT", "Haiti"),("HM", "Heard Island and McDonald Islands"),("VA", "Holy See (Vatican City State)"),("HN", "Honduras"),("HK", "Hong Kong"),("HU", "Hungary"),("IS", "Iceland"),("IN", "India"),("ID", "Indonesia"),("IR", "Iran, Islamic Republic of"),("IQ", "Iraq"),("IE", "Ireland"),("IM", "Isle of Man"),("IL", "Israel"),("IT", "Italy"),("JM", "Jamaica"),("JP", "Japan"),("JE", "Jersey"),("JO", "Jordan"),("KZ", "Kazakhstan"),("KE", "Kenya"),("KI", "Kiribati"),("KP", "Korea, Democratic People's Republic of"),("KR", "Korea, Republic of"),("KW", "Kuwait"),("KG", "Kyrgyzstan"),("LA", "Lao People's Democratic Republic"),("LV", "Latvia"),("LB", "Lebanon"),("LS", "Lesotho"),("LR", "Liberia"),("LY", "Libyan Arab Jamahiriya"),("LI", "Liechtenstein"),("LT", "Lithuania"),("LU", "Luxembourg"),("MO", "Macao"),("MK", "Macedonia, The Former Yugoslav Republic of"),("MG", "Madagascar"),("MW", "Malawi"),("MY", "Malaysia"),("MV", "Maldives"),("ML", "Mali"),("MT", "Malta"),("MH", "Marshall Islands"),("MQ", "Martinique"),("MR", "Mauritania"),("MU", "Mauritius"),("YT", "Mayotte"),("MX", "Mexico"),("FM", "Micronesia, Federated States of"),("MD", "Moldova, Republic of"),("MC", "Monaco"),("MN", "Mongolia"),("ME", "Montenegro"),("MS", "Montserrat"),("MA", "Morocco"),("MZ", "Mozambique"),("MM", "Myanmar"),("NA", "Namibia"),("NR", "Nauru"),("NP", "Nepal"),("NL", "Netherlands"),("NC", "New Caledonia"),("NZ", "New Zealand"),("NI", "Nicaragua"),("NE", "Niger"),("NG", "Nigeria"),("NU", "Niue"),("NF", "Norfolk Island"),("MP", "Northern Mariana Islands"),("NO", "Norway"),("OM", "Oman"),("PK", "Pakistan"),("PW", "Palau"),("PS", "Palestinian Territory, Occupied"),("PA", "Panama"),("PG", "Papua New Guinea"),("PY", "Paraguay"),("PE", "Peru"),("PH", "Philippines"),("PN", "Pitcairn"),("PL", "Poland"),("PT", "Portugal"),("PR", "Puerto Rico"),("QA", "Qatar"),("RE", "Reunion"),("RO", "Romania"),("RU", "Russian Federation"),("RW", "Rwanda"),("BL", "Saint Barthelemy"),("SH", "Saint Helena, Ascension and Tristan Da Cunha"),("KN", "Saint Kitts and Nevis"),("LC", "Saint Lucia"),("MF", "Saint Martin (French Part)"),("PM", "Saint Pierre and Miquelon"),("VC", "Saint Vincent and the Grenadines"),("WS", "Samoa"),("SM", "San Marino"),("ST", "Sao Tome and Principe"),("SA", "Saudi Arabia"),("SN", "Senegal"),("RS", "Serbia"),("SC", "Seychelles"),("SL", "Sierra Leone"),("SG", "Singapore"),("SX", "Sint Maarten (Dutch Part)"),("SK", "Slovakia"),("SI", "Slovenia"),("SB", "Solomon Islands"),("SO", "Somalia"),("ZA", "South Africa"),("GS", "South Georgia and the South Sandwich Islands"),("ES", "Spain"),("LK", "Sri Lanka"),("SD", "Sudan"),("SR", "Suriname"),("SJ", "Svalbard and Jan Mayen"),("SZ", "Swaziland"),("SE", "Sweden"),("CH", "Switzerland"),("SY", "Syrian Arab Republic"),("TW", "Taiwan, Province of China"),("TJ", "Tajikistan"),("TZ", "Tanzania, United Republic of"),("TH", "Thailand"),("TL", "Timor-Leste"),("TG", "Togo"),("TK", "Tokelau"),("TO", "Tonga"),("TT", "Trinidad and Tobago"),("TN", "Tunisia"),("TR", "Turkey"),("TM", "Turkmenistan"),("TC", "Turks and Caicos Islands"),("TV", "Tuvalu"),("UG", "Uganda"),("UA", "Ukraine"),("AE", "United Arab Emirates"),("GB", "United Kingdom"),("US", "United States"),("UM", "United States Minor Outlying Islands"),("UY", "Uruguay"),("UZ", "Uzbekistan"),("VU", "Vanuatu"),("VE", "Venezuela, Bolivarian Republic of"),("VN", "Viet Nam"),("VG", "Virgin Islands, British"),("VI", "Virgin Islands, U.S."),("WF", "Wallis and Futuna"),("EH", "Western Sahara"),("YE", "Yemen"),("ZM", "Zambia"),("ZW", "Zimbabwe"),)
	city = models.CharField(max_length=100, help_text='Limited to 100 characters.')
	state = USStateField(blank=True)
	country = models.CharField(choices=COUNTRY_CHOICES, max_length=5, default=("US"))
	slug = models.SlugField(unique=True)

	class Meta:
		verbose_name = 'city'
		verbose_name_plural = 'cities'
		ordering = ('state', 'city',)

	def __unicode__(self):
		if self.state:
			return '%s, %s' % (self.city, self.state)
		if self.city and self.country:
			return '%s' % (self.city)
		return '%' % (self.city)

class Point(models.Model):
	latitude = models.FloatField(blank=True, null=True, help_text='Use <a href="http://www.getlatlon.com/">Get Lat Lon</a> to find this value.')
	longitude = models.FloatField(blank=True, null=True, help_text='Use <a href="http://www.getlatlon.com/">Get Lat Lon</a> to find this value.')
	address = models.CharField(max_length=200, help_text='Limited to 200 characters.')
	city = models.ForeignKey(City)
	zip = models.CharField(max_length=10, blank=True, help_text='Limited to 10 characters.')

	class Meta:
		verbose_name = 'point'
		verbose_name_plural = 'points'
		ordering = ['address']

	def __unicode__(self):
		return '%s' % self.address

class Place(models.Model):
	STATUS_CHOICES = (
		(0, 'Inactive'),
		(1, 'Active'),
	)
	point = models.ForeignKey(Point)
	prename = models.CharField(max_length=200, help_text="Use this field if there are multiple instances for this location. For example, Awful Arthurs Towers and Awful Arthurs Downtown.", blank=True)
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	nickname = models.CharField(blank=True, max_length=100)
	unit = models.CharField(blank=True, max_length=100, help_text='Suite or Apartment #')
	phone = PhoneNumberField(blank=True)
	external_URL = models.URLField(blank=True, help_text="The URL of the website containing additional information.")
	email = models.EmailField(blank=True)
	description = models.TextField(blank=True)
	parking = models.TextField(blank=True, help_text="A description of the place's parking availability.")
	status = models.IntegerField(choices=STATUS_CHOICES, default=1)
	created = models.DateTimeField(default=datetime.datetime.now)
	modified = models.DateTimeField(auto_now=True)
	place_types = models.ManyToManyField(PlaceType, blank=True)

	class Meta:
		verbose_name_plural = 'places'
		ordering = ['name']

	def __unicode__(self):
		if self.prename:
			return '%s %s' % (self.name, self.prename)
		else:
			return self.name

	def full_name(self):
		"""
		Returns the full name of the place.
		"""
		if self.prename:
			return '%s %s' % (self.name, self.prename)
		else:
			return self.name

	@property
	def city(self):
		return u'%s' % self.point.city

	@property
	def full_title(self):
		return u'%s %s' % (self.prename, self.title)

	@property
	def longitude(self):
		return self.point.longitude

	@property
	def latitude(self):
		return self.point.latitude

	@property
	def address(self):
		return u'%s, %s %s' % (self.point.address, self.point.city, self.point.zip)