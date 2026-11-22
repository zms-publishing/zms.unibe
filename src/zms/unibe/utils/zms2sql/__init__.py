import json
import time
import traceback

from devtools import debug
from sqlmodel import Session, inspect, select

from .tables import process_sql_updates
from ...utils.db import connect_sqldb


def zms2sql(models, zms_context, drop=False, verbose=False):
    for model in models:
        print(f"zms2sql: Transfer {model.__name__}")
        query = model.get_zms_catalog_query()

        sqlengine = connect_sqldb(verbose=verbose)
        with Session(sqlengine) as session:

            t0 = time.time()
            print('--------------------------------------------------------------------------')
            print('Process', model)
    
            # ZMSLangDict SQL table -> merged user, system and agenda lang_dicts
            if query == 'langdict':
                try:
                    import OFS.misc_
                    if hasattr(OFS.misc_.misc_, 'zms'):
                        lang_dict_system = OFS.misc_.misc_.zms['langdict'].get_langdict()
                    else:
                        lang_dict_system = {}
                    lang_dict_user = zms_context.get_lang_dict()
                    lang_dict_agenda = json.loads(zms_context.unibe['agenda-categories.json']())
    
                    lang_dict = lang_dict_user | lang_dict_system | lang_dict_agenda
                    entries = [model.model_validate({"key": key, **val})
                               for key, val in lang_dict.items()  # see agenda-categories.json for conventions 
                               if "@campus.unibe.ch" not in key and key != "ub-agenda"]
    
                    if inspect(sqlengine).has_table(model.__name__.lower()):
                        model.__table__.drop(sqlengine)
                    if not inspect(sqlengine).has_table(model.__name__.lower()):
                        model.__table__.create(sqlengine)
                    session.add_all(entries)
                    session.commit()
    
                except Exception as e:
                    if verbose:
                        debug(f"Error processing {model.__name__}: {e}")
                        traceback.print_exc()
                    continue
    
            # other SQL tables -> process all content models using their queries
            else:
                zmsindex_result = zms_context.zcatalog_index(query)
                process_sql_updates(zmsindex_result, model, drop, verbose)
    
            statement = select(model)
            results = session.exec(statement)
    
            t1 = time.time()
            ts = t1 - t0
            print('--------------------------------------------------------------------------')
            print(model.__name__, f'({len(results.all()):,})', f'{ts:.3f} sec', f'= {ts / 60:.2f} min')
            print('==========================================================================')