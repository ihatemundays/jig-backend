from flask import Flask
from flask.views import MethodView

from neo4j.v1 import GraphDatabase, basic_auth

import pprint

app = Flask(__name__)


class JigAPI(MethodView):
    def get(self, label):
        graph = GraphDatabase('bolt://localhost:7687', auth=basic_auth('neo4j', 'neo4j-server'))

        with graph.session() as session:
            result = session.run('MATCH p=(n:{label})-[r]->(m) RETURN p', label=label)

            for record in result:
                pp = pprint.PrettyPrinter(indent=4)

                pp.pprint(record)


app.add_url_rule('/jig/<string:label>/', view_func=JigAPI.as_view('jig'), methods=['GET'])
app.run(host='0.0.0.0')
