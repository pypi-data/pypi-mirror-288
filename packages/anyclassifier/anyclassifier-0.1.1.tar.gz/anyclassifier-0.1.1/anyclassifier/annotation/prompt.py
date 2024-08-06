from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Label:
    name: str
    desc: str


@dataclass
class Example:
    text: str
    label: str


@dataclass
class AnnotationPrompt:
    task_description: str
    label_definition: List[Label]
    few_shot_examples: Optional[List[Example]] = None

    def get_prompt(self, text: str):
        label_name = [l.name for l in self.label_definition]
        assert len(set(label_name)) == len(self.label_definition), "The name of label has to be unique."
        assert len(set(l.desc for l in self.label_definition)) == len(
            self.label_definition), "The desc of label has to be unique."

        if self.few_shot_examples is not None:
            for fs in self.few_shot_examples:
                assert fs.label in label_name, f"The few shot example is not matching the label: {fs.label}"

        label_defn_str = "\n".join([f"{ld.name}: {ld.desc}" for ld in self.label_definition])
        example_str = "" if self.few_shot_examples is None else "\nHere are some examples:\n" + "\n".join(
            [f"Example {i+1}.\nText: {fse.text}\nLabel: {fse.label}" for i, fse in enumerate(self.few_shot_examples)]
        )
        return f"""{self.task_description}
Here are the label names and description:
{label_defn_str}

Here is the text to be analyzed:
<text>
{text}
</text>
{example_str}
Provide your analysis in the following format:
<analysis>
Label: [Your answer]
</analysis>"""


if __name__ == "__main__":
    prompt = AnnotationPrompt(
        task_description="Classify a text's sentiment.",
        label_definition=[
            Label(name="1", desc='positive sentiment'),
            Label(name="0", desc='negative sentiment')
        ],
        few_shot_examples=[
            Example(text="This is good movie", label="1"),
            Example(text="It is a waste of time.", label="0")
        ]
    )
    print(prompt.get_prompt("It is one of best I ever watched."))
    prompt = AnnotationPrompt(
        task_description="Classify a text's sentiment.",
        label_definition=[
            Label(name="1", desc='positive sentiment'),
            Label(name="0", desc='negative sentiment')
        ]
    )
    print(prompt.get_prompt("It is one of best I ever watched."))
    prompt = AnnotationPrompt(
        task_description="Classify an academic paper into below labels.",
        label_definition=[
        Label(name='0', desc='Commutative Algebra'),
        Label(name='1', desc='Computer Vision'),
        Label(name='2', desc='Artificial Intelligence'),
        Label(name='3', desc='Systems and Control'),
        Label(name='4', desc='Group Theory'),
        Label(name='5', desc='Computational Engineering'),
        Label(name='6', desc='Programming Languages'),
        Label(name='7', desc='Information Theory'),
        Label(name='8', desc='Data Structures'),
        Label(name='9', desc='Neural and Evolutionary'),
        Label(name='10', desc='Statistics Theory'),
    ]
    )
    print(prompt.get_prompt("The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train."))