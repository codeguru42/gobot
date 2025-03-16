import os.path
from pathlib import Path

from black.trans import defaultdict

from encoders.base import get_encoder_by_name


class GoProcessor:
    def __init__(self, encoder, data_directory):
        self.encoder = get_encoder_by_name(encoder, 19)
        self.data_dir = Path(data_directory)

    def load_go_data(self, data_type, num_samples):
        sampler = Sampler(data_dir=self.data_dir)
        data = sampler.draw_data(data_type, num_samples)

        zip_names = set()
        indices_by_zip_name = defaultdict(default_factory=list)
        for filename, index in data:
            zip_names.add(filename)
            indices_by_zip_name[filename].append(index)
            for zip_name in zip_names:
                base_name = zip_name.replace('.tar.gz', '')
                data_file_name = base_name + data_type
                if not os.path.isfile(self.data_dir / data_file_name):
                    self.process_zip(zip_name, data_file_name, indices_by_zip_name[zip_name])
        features_and_labels = self.consolidate_games(data_type, data)
        return features_and_labels
