import random
from otree.api import *

doc = """
For each participant:
    Assign a condition "treatment" or "control"
    Show Consent for everyone
    Show Accuracy nufge for those in "treatment" condition
    Randomize the order of content evaluation tasks (Content1 - Content4)
    Show questionnaire
The page_sequence contains all tasks.
"""


class C(BaseConstants):
    NAME_IN_URL = 'app'
    PLAYERS_PER_GROUP = None
    TASKS = ['Content1', 'Content2', 'Content3', 'Content4']
    NUM_ROUNDS = len(TASKS)+2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Consentimiento
    consent = models.BooleanField(
        choices=[[True, 'Sí, acepto participar y confirmo ser mayor de edad.'], [False, 'No, no deseo participar.']],
        widget=widgets.RadioSelect
    )

    # Unique ID
    id_num = models.StringField()
    
    # Accuracy_nudge (for treatment condition)
        # Nudge response (Solo para grupo de tratamiento)
    nudge_response = models.StringField(
        choices=['True', 'False']
    )

    # Campos para cada contenido
    share_video1_priv = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_video1_pub = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    comment_video1 = models.LongStringField(
        max_length=300
    )
    seen_video1 = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_news1_priv = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_news1_pub = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )
    comment_news1 = models.LongStringField(
        max_length=300
    )
    seen_news1 = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_video2_priv = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_video2_pub = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )
    comment_video2 = models.LongStringField(
        max_length=300
    )
    seen_video2 = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    
    share_news2_priv = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    share_news2_pub = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']]
    )
    comment_news2 = models.LongStringField(
        max_length=300
    )
    seen_news2 = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )


# Cuestionarios y otros campos...    
    crt_question1 = models.FloatField()
    crt_question2 = models.StringField()
    crt_question3 = models.StringField()

    political_position = models.IntegerField(
        min=1,
        max=10
    )

    internet_usage = models.IntegerField(
        min=0,
        max=5
    )

    would_share_news_priv = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )

    would_share_news_pub = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )

    would_share_videos_priv = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )

    would_share_videos_pub = models.BooleanField(
    choices=[[True, 'Yes'], [False, 'No']]
    )
    
    years_education = models.StringField(
        choices=[
            'Less than 5 years',
            'Between 5 and 11 years',
            'Between 12 and 16 years',
            'More than 16 years'
        ]
    )
    age = models.IntegerField(
        min=18,
        max=100
    )
    gender = models.StringField(
        choices=['Male', 'Female', 'Non-binary', 'Other']
    )
    contact = models.StringField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            # Asignar condición de control o tratamiento de forma balanceada
            if p.participant.id_in_session % 2 == 1:
                p.participant.vars['condition'] = 'treatment'
            else:
                p.participant.vars['condition'] = 'control'
            
            # Asignar rondas para las tareas de contenido (rondas 2 a 5)
            round_numbers = list(range(2, C.NUM_ROUNDS))  # Rondas 2 a 5
            random.shuffle(round_numbers)
            task_rounds = dict(zip(C.TASKS, round_numbers))
            print('player', p.id_in_subsession)
            print('condition:', p.participant.vars['condition'])
            print('task_rounds is', task_rounds)
            p.participant.vars['task_rounds'] = task_rounds


# PAGES

class Consent(Page):
    form_model = 'player'
    form_fields = ['id_num','consent']
    
    @staticmethod
    def is_displayed(player: Player):
        # Mostrar solo en la primera ronda
        return player.round_number == 1
    
    def before_next_page(player: Player, timeout_happened):
        # Almacenar el consentimiento en participant.vars
        player.participant.vars['consent'] = player.consent
        if not player.consent:
            # Si el participante no consiente, redirige a la página de declinación
            return 'Decline'

class Decline(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Mostrar solo en la primera ronda y si el participante no consintió
        return player.round_number == 1 and not player.consent
    
    def vars_for_template(player: Player):
        return {}

class trtmnt(Page):
    form_model = 'player'
    form_fields = ['nudge_response']
    
    @staticmethod
    def is_displayed(player: Player):
        # Mostrar solo en la primera ronda, para tratamiento y si consintió
        return (
            player.round_number == 1 and
            player.participant.vars.get('condition') == 'treatment' and
            player.participant.vars.get('consent', False)
        )

    def vars_for_template(player: Player):
        return {}


class Info(Page):
    @staticmethod
    def is_displayed(player: Player):
        """
        Muestra la página de información después de:
        - Consentimiento para el grupo de control.
        - Nudge de precisión para el grupo de tratamiento.
        """
        condition = player.participant.vars.get('condition')
        consent = player.participant.vars.get('consent', False)
        
        # Mostrar Info después de Consent para Control
        if condition == 'control' and player.round_number == 1:
            return consent
        
        # Mostrar Info después de trtmnt para Tratamiento
        if condition == 'treatment' and player.round_number == 1:
            return consent
        
        return False

    def vars_for_template(player: Player):
        return {}

class Content1(Page):
    form_model = 'player'
    form_fields = ['share_video1_priv', 'share_video1_pub', 'comment_video1', 'seen_video1']
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.vars.get('consent', False) and player.round_number == participant.vars['task_rounds'].get('Content1', 0)


class Content2(Page):
    form_model = 'player'
    form_fields = ['share_news1_priv', 'share_news1_pub', 'comment_news1', 'seen_news1']
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.vars.get('consent', False) and player.round_number == participant.vars['task_rounds'].get('Content2', 0)


class Content3(Page):
    form_model = 'player'
    form_fields = ['share_video2_priv', 'share_video2_pub', 'comment_video2', 'seen_video2']
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.vars.get('consent', False) and player.round_number == participant.vars['task_rounds'].get('Content3', 0)


class Content4(Page):
    form_model = 'player'
    form_fields = ['share_news2_priv', 'share_news2_pub', 'comment_news2', 'seen_news2']
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.vars.get('consent', False) and player.round_number == participant.vars['task_rounds'].get('Content4', 0)

class Crt(Page):
    form_model = 'player'
    form_fields = ['crt_question1', 'crt_question2', 'crt_question3']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        return {}

class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'political_position',
        'internet_usage',
        'would_share_news_priv',
        'would_share_news_pub',
        'would_share_videos_priv',
        'would_share_videos_pub',
        'years_education',
        'age',
        'gender'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        return {}


class Contact(Page):
    form_model = 'player'
    form_fields = ['contact']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        return {}

class Endpage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        return {}




page_sequence = [
    Consent,     # Página de consentimiento al inicio (solo ronda 1)
    Decline,     # Página de declinación si el participante no consiente (solo ronda 1)
    trtmnt, # Accuracy nudge
    Info,
    Content1,    # Páginas de contenido aleatorio (rondas 1 a 4)
    Content2,
    Content3,
    Content4,
    Crt,         # Páginas finales que se muestran solo en la última ronda (ronda 5)
    Demographics,
    Contact,
    Endpage,
]
