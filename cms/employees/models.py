from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import *
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from cms.related_links.models import RelatedLink
from markdown import markdown
from cms.static_media.models import Document
from cms.places.models import Place, PlaceType

class Education(models.Model):
	DEGREETYPE_CHOICES = (
		('BA', 'B.A.'),
		('BS', 'B.S.'),
		('AB', 'A.B.'),
		('MA', 'M.A.'),
		('MS', 'M.S.'),
		('MBBS', 'M.B.B.S.'),
		('PHD', 'Ph.D.'),
		('PD', 'Post doctoral fellowship'),
		('MD', 'M.D.'),
	)
	COUNTRY_CHOICES = (("AF", "Afghanistan"),("AX", "Aland Islands"),("AL", "Albania"),("DZ", "Algeria"),("AS", "American Samoa"),("AD", "Andorra"),("AO", "Angola"),("AI", "Anguilla"),("AQ", "Antarctica"),("AG", "Antigua and Barbuda"),("AR", "Argentina"),("AM", "Armenia"),("AW", "Aruba"),("AU", "Australia"),("AT", "Austria"),("AZ", "Azerbaijan"),("BS", "Bahamas"),("BH", "Bahrain"),("BD", "Bangladesh"),("BB", "Barbados"),("BY", "Belarus"),("BE", "Belgium"),("BZ", "Belize"),("BJ", "Benin"),("BM", "Bermuda"),("BT", "Bhutan"),("BO", "Bolivia, Plurinational State of"),("BQ", "Bonaire, Saint Eustatius and Saba"),("BA", "Bosnia and Herzegovina"),("BW", "Botswana"),("BV", "Bouvet Island"),("BR", "Brazil"),("IO", "British Indian Ocean Territory"),("BN", "Brunei Darussalam"),("BG", "Bulgaria"),("BF", "Burkina Faso"),("BI", "Burundi"),("KH", "Cambodia"),("CM", "Cameroon"),("CA", "Canada"),("CV", "Cape Verde"),("KY", "Cayman Islands"),("CF", "Central African Republic"),("TD", "Chad"),("CL", "Chile"),("CN", "China"),("CX", "Christmas Island"),("CC", "Cocos (Keeling) Islands"),("CO", "Colombia"),("KM", "Comoros"),("CG", "Congo"),("CD", "Congo, The Democratic Republic of the"),("CK", "Cook Islands"),("CR", "Costa Rica"),("CI", "Cote D'ivoire"),("HR", "Croatia"),("CU", "Cuba"),("CW", "Curacao"),("CY", "Cyprus"),("CZ", "Czech Republic"),("DK", "Denmark"),("DJ", "Djibouti"),("DM", "Dominica"),("DO", "Dominican Republic"),("EC", "Ecuador"),("EG", "Egypt"),("SV", "El Salvador"),("GQ", "Equatorial Guinea"),("ER", "Eritrea"),("EE", "Estonia"),("ET", "Ethiopia"),("FK", "Falkland Islands (Malvinas)"),("FO", "Faroe Islands"),("FJ", "Fiji"),("FI", "Finland"),("FR", "France"),("GF", "French Guiana"),("PF", "French Polynesia"),("TF", "French Southern Territories"),("GA", "Gabon"),("GM", "Gambia"),("GE", "Georgia"),("DE", "Germany"),("GH", "Ghana"),("GI", "Gibraltar"),("GR", "Greece"),("GL", "Greenland"),("GD", "Grenada"),("GP", "Guadeloupe"),("GU", "Guam"),("GT", "Guatemala"),("GG", "Guernsey"),("GN", "Guinea"),("GW", "Guinea-Bissau"),("GY", "Guyana"),("HT", "Haiti"),("HM", "Heard Island and McDonald Islands"),("VA", "Holy See (Vatican City State)"),("HN", "Honduras"),("HK", "Hong Kong"),("HU", "Hungary"),("IS", "Iceland"),("IN", "India"),("ID", "Indonesia"),("IR", "Iran, Islamic Republic of"),("IQ", "Iraq"),("IE", "Ireland"),("IM", "Isle of Man"),("IL", "Israel"),("IT", "Italy"),("JM", "Jamaica"),("JP", "Japan"),("JE", "Jersey"),("JO", "Jordan"),("KZ", "Kazakhstan"),("KE", "Kenya"),("KI", "Kiribati"),("KP", "Korea, Democratic People's Republic of"),("KR", "Korea, Republic of"),("KW", "Kuwait"),("KG", "Kyrgyzstan"),("LA", "Lao People's Democratic Republic"),("LV", "Latvia"),("LB", "Lebanon"),("LS", "Lesotho"),("LR", "Liberia"),("LY", "Libyan Arab Jamahiriya"),("LI", "Liechtenstein"),("LT", "Lithuania"),("LU", "Luxembourg"),("MO", "Macao"),("MK", "Macedonia, The Former Yugoslav Republic of"),("MG", "Madagascar"),("MW", "Malawi"),("MY", "Malaysia"),("MV", "Maldives"),("ML", "Mali"),("MT", "Malta"),("MH", "Marshall Islands"),("MQ", "Martinique"),("MR", "Mauritania"),("MU", "Mauritius"),("YT", "Mayotte"),("MX", "Mexico"),("FM", "Micronesia, Federated States of"),("MD", "Moldova, Republic of"),("MC", "Monaco"),("MN", "Mongolia"),("ME", "Montenegro"),("MS", "Montserrat"),("MA", "Morocco"),("MZ", "Mozambique"),("MM", "Myanmar"),("NA", "Namibia"),("NR", "Nauru"),("NP", "Nepal"),("NL", "Netherlands"),("NC", "New Caledonia"),("NZ", "New Zealand"),("NI", "Nicaragua"),("NE", "Niger"),("NG", "Nigeria"),("NU", "Niue"),("NF", "Norfolk Island"),("MP", "Northern Mariana Islands"),("NO", "Norway"),("OM", "Oman"),("PK", "Pakistan"),("PW", "Palau"),("PS", "Palestinian Territory, Occupied"),("PA", "Panama"),("PG", "Papua New Guinea"),("PY", "Paraguay"),("PE", "Peru"),("PH", "Philippines"),("PN", "Pitcairn"),("PL", "Poland"),("PT", "Portugal"),("PR", "Puerto Rico"),("QA", "Qatar"),("RE", "Reunion"),("RO", "Romania"),("RU", "Russian Federation"),("RW", "Rwanda"),("BL", "Saint Barthelemy"),("SH", "Saint Helena, Ascension and Tristan Da Cunha"),("KN", "Saint Kitts and Nevis"),("LC", "Saint Lucia"),("MF", "Saint Martin (French Part)"),("PM", "Saint Pierre and Miquelon"),("VC", "Saint Vincent and the Grenadines"),("WS", "Samoa"),("SM", "San Marino"),("ST", "Sao Tome and Principe"),("SA", "Saudi Arabia"),("SN", "Senegal"),("RS", "Serbia"),("SC", "Seychelles"),("SL", "Sierra Leone"),("SG", "Singapore"),("SX", "Sint Maarten (Dutch Part)"),("SK", "Slovakia"),("SI", "Slovenia"),("SB", "Solomon Islands"),("SO", "Somalia"),("ZA", "South Africa"),("GS", "South Georgia and the South Sandwich Islands"),("ES", "Spain"),("LK", "Sri Lanka"),("SD", "Sudan"),("SR", "Suriname"),("SJ", "Svalbard and Jan Mayen"),("SZ", "Swaziland"),("SE", "Sweden"),("CH", "Switzerland"),("SY", "Syrian Arab Republic"),("TW", "Taiwan, Province of China"),("TJ", "Tajikistan"),("TZ", "Tanzania, United Republic of"),("TH", "Thailand"),("TL", "Timor-Leste"),("TG", "Togo"),("TK", "Tokelau"),("TO", "Tonga"),("TT", "Trinidad and Tobago"),("TN", "Tunisia"),("TR", "Turkey"),("TM", "Turkmenistan"),("TC", "Turks and Caicos Islands"),("TV", "Tuvalu"),("UG", "Uganda"),("UA", "Ukraine"),("AE", "United Arab Emirates"),("GB", "United Kingdom"),("US", "United States"),("UM", "United States Minor Outlying Islands"),("UY", "Uruguay"),("UZ", "Uzbekistan"),("VU", "Vanuatu"),("VE", "Venezuela, Bolivarian Republic of"),("VN", "Viet Nam"),("VG", "Virgin Islands, British"),("VI", "Virgin Islands, U.S."),("WF", "Wallis and Futuna"),("EH", "Western Sahara"),("YE", "Yemen"),("ZM", "Zambia"),("ZW", "Zimbabwe"),)

	country = models.CharField(choices=COUNTRY_CHOICES, max_length=5, default=("US"))
	state = USStateField(blank=True)
	field_of_study = models.CharField(max_length=250, help_text='Limited to 250 characters.', blank=True)
	date_earned = models.DateField(help_text='To specify only the year, simply type in the date using the following format: 2011-01-01.', blank=True, null=True)
	degree_type = models.CharField(max_length=5, choices=DEGREETYPE_CHOICES)
	school = models.ForeignKey(Place)
	additional_notes = models.TextField(blank=True)
	employee_attended = models.ForeignKey('Employee')

	class Meta:
		verbose_name_plural = 'Education'

class FeaturedPublicationManager(models.Manager):
	def get_query_set(self):
		return super(FeaturedPublicationManager, self).get_query_set().filter(is_featured=True)

class Publication(models.Model):
	BOOK_CHAPTER = 1
	ARTICLE = 2
	PUBLICATION_CHOICES = (
		(BOOK_CHAPTER, 'Book chapter'),
		(ARTICLE, 'Article'),
	)
	publication_type = models.IntegerField(choices=PUBLICATION_CHOICES)
	article_title = models.CharField(max_length=250, help_text='Limited to 250 characters.', verbose_name="publication title")
	slug = models.SlugField(help_text='Suggested value automatically generated from title.')
	primary_author = models.ForeignKey('Employee', limit_choices_to={'employee_type': 1}, help_text='Most of the time, this will be the faculty member to whom the publication is tied.')
	authors = models.CharField(max_length=250, help_text='Limited to 250 characters. Please adhere to accepted format for style. Include current employee in this list.', blank=True)
	journal_name = models.CharField(max_length=250, help_text='Limited to 250 characters. May also be used for book titles.')
	journal_volume = models.IntegerField(max_length=3, blank=True, null=True)
	journal_issue = models.IntegerField(max_length=3, blank=True, null=True)
	journal_pub_date = models.DateField(help_text='To specify only the year, simply type in the date using the following format: 2011-01-01.')
	journal_page_range = models.CharField(max_length=50, help_text='Limited to 50 characters.', blank=True)
	editors = models.CharField(max_length=250, help_text='Limited to 250 characters.', blank=True)
	publisher = models.CharField(max_length=250, help_text='Limited to 250 characters.', blank=True)
	location_of_publication = models.CharField(max_length=250, help_text='Limited to 250 characters.', blank=True)
	abstract = models.TextField(blank=True)
	notes = models.TextField(blank=True)
	external_link = models.URLField(blank=True, help_text='Link to the article on the publication\'s website.')
	downloadable_version = models.ForeignKey(Document, blank=True, null=True)
	is_featured = models.BooleanField(default=False, help_text='Check this box to show this publication on the primary author\'s profile. Otherwise, it will only show in the list of publications for the primary author. There is a limit to five featured publications per primary author.')
	objects = models.Manager()
	featured = FeaturedPublicationManager()
	
	class Meta:
		verbose_name_plural = 'Publications'
		ordering = ['-journal_pub_date']
		unique_together = (("slug", "primary_author"),)
		
	def __unicode__(self):
		return self.article_title

class EmployedEmployeeManager(models.Manager):
	def get_query_set(self):
		return super(EmployedEmployeeManager, self).get_query_set().filter(is_currently_employed=True)

class Employee(models.Model):
	FACULTY = 1
	ADMINISTRATIVE_SUPPORT = 2
	RESEARCH_SUPPORT = 3
	POSTDOCS = 4
	EMPLOYEE_CHOICES = (
		(FACULTY, 'Faculty'),
		(ADMINISTRATIVE_SUPPORT, 'Administrative support'),
		(RESEARCH_SUPPORT, 'Research support'),
		(POSTDOCS, 'Postdocs'),
	)
	user = models.ForeignKey(User, unique=True, help_text="Select a user if this employee is able to update their own profile information.", blank=True, null=True)

	first_name = models.CharField(max_length=200)
	middle_name = models.CharField(max_length=50, help_text="Limited to 50 characters.", blank=True)
	last_name = models.CharField(max_length=200)

	slug = models.SlugField(unique=True, help_text='Will populate from a combination of the first, middle and last names.')
	
	title = models.CharField(max_length=200, help_text="Limited to 200 characters.")
	previous_position = models.CharField(max_length=350, help_text="Limited to 350 characters.", blank=True)
	
	email = models.EmailField(blank=True)
	office_phone_number = PhoneNumberField(null=True, blank=True)
	mobile_phone_number = PhoneNumberField(null=True, blank=True)
	office = models.CharField(max_length=50, help_text="Your office number or room name. Limited to 50 characters.", blank=True)
	website = models.URLField(blank=True)
	
	job_description = models.TextField(help_text='A description of your work or research. No HTML is allowed. If formatting is needed, please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.', blank=True)
	job_description_html = models.TextField(blank=True, editable=False)
	
	job_description_summary = models.CharField(max_length=250, help_text="A brief summary of your work or research. Limited to 250 characters.")
	
	is_currently_employed = models.BooleanField(default=True)
	related_links = generic.GenericRelation(RelatedLink, blank=True)
	employee_type = models.IntegerField(choices=EMPLOYEE_CHOICES)
	
	photo = models.ImageField(upload_to='images/profiles/mugshots', blank=True)
	lead_image = models.ImageField(upload_to='images/profiles/graphics', blank=True)
	
	resume_or_cv = models.ForeignKey(Document, blank=True, null=True)
	
	sites = models.ManyToManyField(Site)

	objects = models.Manager()
	employed = EmployedEmployeeManager()
	
	class Meta:
		verbose_name_plural = 'Employees'
		ordering = ['last_name']
	
	def __unicode__(self):
		return self.slug

	def get_absolute_url(self):
		return '/employees/%s/' % (self.slug)

	@property
	def get_stories_for_faculty(self):
		return self.stories_for_subject.filter(status=1)

	def save(self):
		self.job_description_html = markdown(self.job_description)
		super(Employee, self).save()