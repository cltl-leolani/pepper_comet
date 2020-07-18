from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse, abort

from inference import AtomicInference, ConceptNetInference

# Use the CPU
import sys
import os
sys.path.append(os.getcwd())
import src.data.config
src.data.config.device = "cpu"


def app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='COMET API',
        description='COMET common knowledge inference')

    return app, api


def arg_parser():
    parser = reqparse.RequestParser()
    relations_help = get_relations_help(atomic_inference.get_relations(),
            conceptnet_inference.get_relations())
    parser.add_argument('event', required=True, help=get_event_help())
    parser.add_argument('rel', action='append', required=False, default=['all'], help=relations_help)
    parser.add_argument('sample', required=False, default='greedy', help=get_sampling_help())

    return parser


def response_models(atomic_inference, conceptnet_inference):
    atomic_entry = api.model('AtomicEntry', {
            'event': fields.String,
            'beams': fields.List(fields.String),
    })
    atomic_model = api.model('Atomic',
            { rel: fields.Nested(atomic_entry, skip_none=True)
              for rel in atomic_inference.get_relations() })

    conceptnet_entry = api.model('ConceptNetEntry', {
            'event': fields.String(attribute='e1'),
            'beams': fields.List(fields.String),
    })
    conceptnet_model = api.model('ConceptNet',
            { rel: fields.Nested(conceptnet_entry, skip_none=True)
              for rel in conceptnet_inference.get_relations() })

    return atomic_model, conceptnet_model


def get_event_help():
    return """\"atomic\":
        Provide a seed event such as \"PersonX goes to the mall\"
        Don't include names, instead replacing them with PersonX, PersonY, etc.
        The event should always have PersonX included
    \"conceptnet\":
        Provide a seed entity such as \"go to the mall\"
        Because the model was trained on lemmatized entities,
        it works best if the input entities are also lemmatized
    """

def get_relations_help(atomic_relations, conceptnet_relations):
    return """\"atomic\":
        Enter a possible effect type from the following effect types:
        all - compute the output for all effect types
        {}
    \"conceptnet\":
        Enter a possible relation from the following list:
        all - compute the output for all effect types
        {}
        NOTE: Capitalization is important
    """.format(
            "".join(rel + "\n" for rel in atomic_relations),
            "".join(rel + "\n" for rel in conceptnet_relations)
    )

def get_sampling_help():
    return """Provide a sampling algorithm to produce the sequence with from the following:
    greedy
    beam-# where # is the beam size
    topk-# where # is k
    """



atomic_inference = AtomicInference()
conceptnet_inference = ConceptNetInference()
app, api = app()
parser = arg_parser()
atomic_model, conceptnet_model = response_models(atomic_inference, conceptnet_inference)


@api.route('/api/atomic/infer')
@api.expect(parser)
class Atomic(Resource):
    @api.marshal_with(atomic_model, skip_none=True)
    def get(self):
        args = parser.parse_args(request)

        return atomic_inference.infer(args['event'], args['rel'], args['sample'])

@api.route('/api/conceptnet/infer')
@api.expect(parser)
class Conceptnet(Resource):
    @api.marshal_with(conceptnet_model, skip_none=True)
    def get(self):
        args = parser.parse_args(request)

        return conceptnet_inference.infer(args['event'], args['rel'], args['sample'])
