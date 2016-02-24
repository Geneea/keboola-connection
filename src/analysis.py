# coding=utf-8

import csv
import sys

import correction
import entities
import hashtags
import language
import lemmatize
import mainTools
import sentiment
import topic

ANALYSIS = {
    'language': language,
    'lemmatize': lemmatize,
    'correction': correction,
    'topic': topic,
    'sentiment': sentiment,
    'entities': entities,
    'hashtags': hashtags
}

if __name__ == '__main__':
    output_files = dict()
    try:
        config = mainTools.parse_config()
        if not isinstance(config.analysis_types, list) or len(config.analysis_types) == 0:
            raise LookupError("the analysis_types must be provided")

        types = map(lambda t: str(t).lower(), config.analysis_types)
        for analysis_type in types:
            if analysis_type not in ANALYSIS.keys():
                raise LookupError("unknown analysis type '{t}'".format(t=analysis_type))

        output_files = {t: open("{path}{t}.csv".format(path=config.output_path, t=t), 'wb') for t in types}
        with open(config.input_path, 'rb') as input_file:
            reader = mainTools.unfussy_csv_reader(input_file)

            writers = dict()
            for analysis_type in types:
                csv_header = [config.id_col] + ANALYSIS[analysis_type].csv_header()
                writers[analysis_type] = csv.DictWriter(output_files[analysis_type], fieldnames=csv_header)
                writers[analysis_type].writeheader()

            for rows in mainTools.slice_stream(reader, mainTools.DOC_BATCH_SIZE):
                for doc in mainTools.make_request(config, 'analysis', rows):
                    for analysis_type in types:
                        res = doc['analysisByType'][analysis_type]
                        for res_row in ANALYSIS[analysis_type].create_results(res):
                            res_row[config.id_col] = doc['id'].encode('utf-8')
                            writers[analysis_type].writerow(res_row)

        print >> sys.stdout, "the analysis finished"
        sys.exit(0)
    except (LookupError, IOError) as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(1)
    except Exception as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(2)
    finally:
        for f in output_files.values():
            f.close()
