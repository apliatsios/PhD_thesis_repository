#!/usr/bin/python
# -*- coding: utf-8 -*-
#Snap4City: IoT-Directory
# Copyright (C) 2017 DISIT Lab https://www.disit.org - University of Florence

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

Converts an NGSI v2 Normalized Representation
into an NGSI-LD Representation

Copyright (c) 2018 FIWARE Foundation e.V.

Author: José Manuel Cantera

"""

import sys
import json

from rfc3987 import parse

etsi_core_context = 'https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld'


def ngsild_uri(type_part, id_part):
    template = 'urn:ngsi-ld:{}:{}'

    return template.format(type_part, id_part)


# Generates an Entity Id as a URI
def ld_id(entity_id, entity_type):
    out = entity_id
    try:
        d = parse(entity_id, rule='URI')
        scheme = d['scheme']
        if scheme != 'urn' and scheme != 'http' and scheme != 'https':
            raise ValueError
    except ValueError:
        out = ngsild_uri(entity_type, entity_id)

    return out


# Generates a Relationship's object as a URI
def ld_object(attribute_name, entity_id):
    out = entity_id
    try:
        d = parse(entity_id, rule='URI')
        scheme = d['scheme']
        if scheme != 'urn' and scheme != 'http' and scheme != 'https':
            raise ValueError
    except ValueError:
        entity_type = ''
        if attribute_name.startswith('ref'):
            entity_type = attribute_name[3:]

        out = ngsild_uri(entity_type, entity_id)

    return out


# Do all the transformation work
def normalized_2_LD(entity, ld_context_uri):
    out = {
        '@context': [ld_context_uri, etsi_core_context]
    }

    for key in entity:
        if key == 'id':
            out[key] = ld_id(entity['id'], entity['type'])
            continue

        if key == 'type':
            out[key] = entity[key]
            continue

        if key == 'dateCreated':
            out['createdAt'] = normalize_date(entity[key]['value'])
            continue

        if key == 'dateModified':
            out['modifiedAt'] = normalize_date(entity[key]['value'])
            continue

        attr = entity[key]
        out[key] = {}
        ld_attr = out[key]

        if not ('type' in attr) or attr['type'] != 'Relationship':
            ld_attr['type'] = 'Property'
            ld_attr['value'] = attr['value']
        else:
            ld_attr['type'] = 'Relationship'
            aux_obj = attr['value']
            if isinstance(aux_obj, list):
                ld_attr['object'] = list()
                for obj in aux_obj:
                    ld_attr['object'].append(ld_object(key, obj))
            else:
                ld_attr['object'] = ld_object(key, str(aux_obj))

        if key == 'location':
            ld_attr['type'] = 'GeoProperty'

        if 'type' in attr and attr['type'] == 'DateTime':
            ld_attr['value'] = {
                '@type': 'DateTime',
                '@value': normalize_date(attr['value'])
            }

        if 'type' in attr and attr['type'] == 'PostalAddress':
            ld_attr['value']['type'] = 'PostalAddress'

        if 'metadata' in attr:
            metadata = attr['metadata']

            for mkey in metadata:
                if mkey == 'timestamp':
                    ld_attr['observedAt'] = normalize_date(
                        metadata[mkey]['value'])
                elif mkey == 'unitCode':
                    ld_attr['unitCode'] = metadata[mkey]['value']
                else:
                    sub_attr = dict()
                    # Metadata which are Relationships is assumed not to be there
                    sub_attr['type'] = 'Property'
                    sub_attr['value'] = metadata[mkey]['value']
                    ld_attr[mkey] = sub_attr

    return out


def normalize_date(date_str):
    out = date_str

    if not date_str.endswith('Z'):
        out += 'Z'

    return out


def read_json(infile):
    with open(infile) as data_file:
        data = json.loads(data_file.read())

    return data


def write_json(data, outfile):
    with open(outfile, 'w') as data_file:
        data_file.write("\n")


def main(args):
    data = read_json(args[1])
    result = normalized_2_LD(data, args[3])
    write_json(result, args[2])


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            "Usage: normalized2LD [input file] [output file] [target ld_context]")
        exit(-1)

    main(sys.argv)
