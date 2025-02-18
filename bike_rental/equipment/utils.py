from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from .models import Bike, Accessory
import os
from django.conf import settings
from django.http import HttpResponse
from lxml import etree
from django.contrib.auth.decorators import user_passes_test


def equipment_list_xml():
    bikes = Bike.objects.all()
    accessories = Accessory.objects.all()
    
    root = Element('Equipment')
    bikes_element = SubElement(root, 'bikes')
    accessories_element = SubElement(root, 'accessories')
    
    for bike in bikes:
        bike_element = SubElement(bikes_element, 'bike', category="bike")
        SubElement(bike_element, 'bike_type').text = bike.bike_type
        SubElement(bike_element, 'gear_num').text = str(bike.gear_num)
        SubElement(bike_element, 'usage').text = bike.usage
        SubElement(bike_element, 'has_bell').text = str(bike.has_bell)
        SubElement(bike_element, 'has_trunk').text = str(bike.has_trunk)
        SubElement(bike_element, 'weight').text = str(bike.weight)
        SubElement(bike_element, 'wheel_size_cm').text = str(bike.wheel_size_cm)
        SubElement(bike_element, 'brake_type').text = bike.brake_type or ''
        SubElement(bike_element, 'price_for_one_day').text = str(bike.price_for_one_day)
        SubElement(bike_element, 'quantity').text = str(bike.quantity)
        SubElement(bike_element, 'brand').text = bike.brand
        SubElement(bike_element, 'additional_info').text = bike.additional_info or ''
        SubElement(bike_element, 'person').text = bike.person

    
    for accessory in accessories:
        accessory_element = SubElement(accessories_element, 'accessory', category="accessory")
        SubElement(accessory_element, 'accessory_type').text = accessory.accessory_type
        SubElement(accessory_element, 'price_for_one_day').text = str(accessory.price_for_one_day)
        SubElement(accessory_element, 'quantity').text = str(accessory.quantity)
        SubElement(accessory_element, 'brand').text = accessory.brand
        SubElement(accessory_element, 'additional_info').text = accessory.additional_info or ''
        SubElement(accessory_element, 'person').text = accessory.person
    
    xml_string = tostring(root, 'utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

    return pretty_xml

def save_equipment_xml(xml_data):
    directory = os.path.join(settings.BASE_DIR, 'generated_xmls')
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = 'equipment.xml'
    file_path = os.path.join(directory, file_name)

    with open(file_path, 'wb') as file:
        file.write(xml_data.encode('utf-8'))

    return file_name

def generate_xml():
    xml_data = equipment_list_xml()
    file_name = save_equipment_xml(xml_data)
    
    response = HttpResponse("File saved", content_type='text/plain')
    return response

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def render_xml_with_xsl(request):
    xml_file_path = os.path.join(settings.BASE_DIR, 'generated_xmls', 'equipment.xml')
    xsl_file_path = os.path.join(settings.BASE_DIR, 'generated_xmls', 'equipment.xsl')
    
    xml_doc = etree.parse(xml_file_path)
    xsl_doc = etree.parse(xsl_file_path)
    
    transform = etree.XSLT(xsl_doc)
    
    transformed = transform(xml_doc)
    
    return HttpResponse(str(transformed), content_type='text/html')

