import os
import sys
sys.path.append(os.getcwd())

import src.data.data as data
import src.interactive.functions as interactive

DEFAULT_ATOMIC_MODEL = "pretrained_models/atomic_pretrained_model.pickle"
DEFAULT_CONCEPTNET_MODEL = "pretrained_models/conceptnet_pretrained_model.pickle"



class Inference:
    def __init__(self, inference_type, model_file):
        self._opt, state_dict = interactive.load_model_file(model_file)

        self._data_loader, self._text_encoder = interactive.load_data(inference_type, self._opt)

        n_ctx = self._get_n_ctx(self._data_loader)
        n_vocab = len(self._text_encoder.encoder) + n_ctx
        self._model = interactive.make_model(self._opt, n_vocab, n_ctx, state_dict)

    def _get_n_ctx(self, data_loader):
        raise NotImplementedError()

    def get_relations(self):
        raise NotImplementedError()

    def infer(self, event, relations=['all'], sampling_algorithm='greedy'):
        sampler = interactive.set_sampler(self._opt, sampling_algorithm, self._data_loader)

        if isinstance(relations, str):
            relations = [relations]

        if not 'all' in relations and not set(relations) <= self.get_relations():
            raise ValueError(set(relations) - self.get_relations())

        return self._get_sequence(event, relations, sampler)

    def _get_sequence(self, event, relations, sampler):
        raise NotImplementedError()


class AtomicInference(Inference):
    def __init__(self, model_file=DEFAULT_ATOMIC_MODEL):
        super().__init__("atomic", model_file)

    def get_relations(self):
        return set(self._data_loader.categories)

    def _get_n_ctx(self, data_loader):
        return self._data_loader.max_event + self._data_loader.max_effect

    def _get_sequence(self, event, relations, sampler):
        return interactive.get_atomic_sequence(
                event, self._model, sampler, self._data_loader, self._text_encoder, relations)


class ConceptNetInference(Inference):
    def __init__(self, model_file=DEFAULT_CONCEPTNET_MODEL):
        super().__init__("conceptnet", model_file)

    def get_relations(self):
        return set(data.conceptnet_data.conceptnet_relations)

    def _get_n_ctx(self, data_loader):
        return data_loader.max_e1 + data_loader.max_e2 + data_loader.max_r

    def _get_sequence(self, event, relations, sampler):
        return interactive.get_conceptnet_sequence(
                event, self._model, sampler, self._data_loader, self._text_encoder, relations)
