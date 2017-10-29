from flask import Flask, abort
from flask.views import MethodView

from neo4j.v1 import GraphDatabase, basic_auth

import pprint

app = Flask(__name__)
graph = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'neo4j-server'))

class JigAPI(MethodView):
    def get(self, label):
        try:
            with graph.session() as session:
                result = session.run('MATCH p=(n:%s)-[r]->(m) RETURN p' % label)

                for record in result:
                    pp = pprint.PrettyPrinter(indent=4)

                    pp.pprint(record)
        except Exception as exception:
            abort(400, exception)

app.add_url_rule('/jig/<string:label>/', view_func=JigAPI.as_view('jig'), methods=['GET'])
app.run(host='0.0.0.0')
