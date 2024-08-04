import re

from .log_formats import colorized_logger
logger = colorized_logger(__name__)


def normalize_name_label(string):
    string = re.sub('[ \-]', '_', string)
    string = string.lower()
    return string


class ADISchemaSourceBasicChecker:
    def validate(self, tables):
        ADISchemaSourceBasicChecker.check_individual_names_labels(tables)
        ADISchemaSourceBasicChecker.check_identification_capability(tables)
        ADISchemaSourceBasicChecker.check_definition_presence(tables)
        ADISchemaSourceBasicChecker.check_field_ordinality(tables['fields'])
        ADISchemaSourceBasicChecker.check_relationship_integrity(tables)

    @staticmethod
    def check_individual_names_labels(tables):
        for tablename, table in tables.items():
            if tablename == 'verbalizations':
                continue
            offenders = [
                name for name in table['Name']
                if not re.match('^[a-zA-Z][a-zA-Z0-9_ ]+$', name)
            ]
            if len(offenders) > 0:
                for offender in offenders:
                    logger.warn(
                        'Name value "%s" (in "%s") has some invalid characters or an invalid initial character.',
                        offender,
                        tablename,
                    )

            offenders = [
                name for name in table['Label']
                if not re.match('^[a-zA-Z][a-zA-Z0-9_ ]+$', name)
            ]
            if len(offenders) > 0:
                for offender in offenders:
                    logger.warn(
                        'Label value "%s" (in "%s") has some invalid characters or an invalid initial character.',
                        offender,
                        tablename,
                    )

    @staticmethod
    def check_identification_capability(tables):
        for tablename, table in tables.items():
            if tablename == 'verbalizations':
                continue
            for i, row in table.iterrows():
                n1 = normalize_name_label(row['Name'])
                n2 = normalize_name_label(row['Label'])
                if n1 != n2:
                    logger.warn(
                        'Name value "%s" and Label value "%s" (in "%s") do not have common reduction; will not be interchangeable in principle.',
                        row['Name'],
                        row['Label'],
                        tablename,
                    )

            all_names = list(set([str(name) for name in table['Name']]))
            all_labels = list(set([str(name) for name in table['Label']]))

            all_names_normalized = list(set([normalize_name_label(name) for name in table['Name']]))
            all_labels_normalized = list(set([normalize_name_label(name) for name in table['Label']]))

            if tablename in ['tables', 'entities', 'properties']:
                if len(all_names) != table.shape[0]:
                    logger.warn('Name tokens have some duplicates in table "%s".', tablename)
                if len(all_labels) != table.shape[0]:
                    logger.warn('Label tokens have some duplicates in table "%s".', tablename)
                if len(all_names_normalized) != table.shape[0]:
                    logger.warn('Normalized Name tokens have some duplicates in table "%s".', tablename)
                if len(all_labels_normalized) != table.shape[0]:
                    logger.warn('Normalized Label tokens have some duplicates in table "%s".', tablename)

        for tablename, fields in tables['fields'].groupby('Table'):
            size_main_key = sum([1 for p in fields['Primary key group'] if p in [1, '1']])
            if size_main_key > 1:
                logger.error('Table "%s" has multi-element main primary key (denoted 1).', tablename)

    @staticmethod
    def check_definition_presence(tables):
        for tablename, table in tables.items():

            if tablename in ['entities', 'properties', 'values']:
                missing_definitions = [
                    row['Label']
                    for i, row in table.iterrows()
                    if row['Definition'] == ''
                ]
                if len(missing_definitions) > 0:
                    for label in missing_definitions:
                        logger.warn(
                            '"%s" (%s) is missing a definition.',
                            label,
                            tablename,
                        )
                    logger.error('Some "%s" are missing definitions.', tablename)

    @staticmethod
    def check_field_ordinality(fields):
        previous_ordinality = None
        previous_table = None
        for i, row in fields.iterrows():
            ordinality = row['Ordinality']
            table = row['Table']
            if previous_table != table:
                if ordinality != 1:
                    logger.warn(
                        'First "Ordinality" value in "fields" (of "%s") is not 1.',
                        table,
                    )
                previous_ordinality = ordinality
                previous_table = table
                continue
            else:
                if ordinality != previous_ordinality + 1:
                    logger.warn(
                        'Fields of "%s" are not in order.',
                        table,
                    )
                previous_ordinality = ordinality
                previous_table = table

    @staticmethod
    def check_relationship_integrity(tables):
        foreign_key_relationships = {
            'Table definitions referencing entity types for the records' : ['tables', tables['tables'], 'Entity', [tables['entities'], tables['entities']], ['Name', 'Label'], 'entities', 'entity'],
            'Field definitions referencing parent tables' : ['fields', tables['fields'], 'Table', [tables['tables'], tables['tables']], ['Name', 'Label'], 'tables', 'table'],
            'Field definitions referencing property types' : ['fields', tables['fields'], 'Property', [tables['properties'], tables['properties'], tables['entities'], tables['entities']], ['Name', 'Label', 'Name', 'Label'], 'properties/entities', 'property/entity'],
            'Field definitions referencing foreign tables' : ['fields', tables['fields'], 'Foreign table', [tables['tables'], tables['tables']], ['Name', 'Label'], 'tables', 'table'],
            'Property definitions referencing entities to which they apply' : ['properties', tables['properties'], 'Entity', [tables['entities'], tables['entities']], ['Name', 'Label'], 'entities', 'entity'],
            'Property definitions referencing target entity types' : ['properties', tables['properties'], 'Related entity', [tables['entities'], tables['entities']], ['Name', 'Label'], 'entities', 'entity'],
            'Value definitions referencing parent property types' : ['values', tables['values'], 'Parent property', [tables['properties'], tables['properties']], ['Name', 'Label'], 'properties', 'property'],
        }
        logger.info('Checking foreign key integrity in schema definition.')
        checks = {
            relationship : ADISchemaSourceBasicChecker.check_mismatched_foreign_keys(*args)
            for relationship, args in foreign_key_relationships.items()
        }
        for relationship, valid in checks.items():
            validation = 'PASS' if valid else 'FAIL'
            if valid:
                logger.info('%s: %s', validation, relationship)
            else:
                logger.error('%s: %s', validation, relationship)

    @staticmethod
    def check_mismatched_foreign_keys(main_tablename, table, column, target_tables, target_columns, referenced_plural, referenced_singular):
        target_identifier_tokens = []
        for i in range(len(target_tables)):
            target_table = target_tables[i]
            target_column = target_columns[i]
            target_identifier_tokens = target_identifier_tokens + list(target_table[target_column])
        mismatched = []
        for i, row in table.iterrows():
            if not row[column] in target_identifier_tokens:
                mismatched.append(row[column])

        mismatched = sorted(list(set(mismatched).difference([''])))
        if len(mismatched) > 1:
            logger.error(
                '%s referenced in "%s.tsv -> %s", but these %s do not exist.',
                mismatched,
                main_tablename,
                column,
                referenced_plural,
            )
            return False
        elif len(mismatched) == 1:
            logger.error(
                '"%s" referenced in "%s.tsv -> %s", but this %s does not exist.',
                mismatched[0],
                main_tablename,
                column,
                referenced_singular,
            )
            return False
        return True
