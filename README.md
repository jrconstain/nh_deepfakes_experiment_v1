# Non-Harmful Deepfakes Experiment

## Research Description

This study aims to evaluate the effectiveness of an accuracy nudge intervention in reducing the sharing and belief of misinformation, particularly in the form of non-harmful deepfake videos and false news headlines. The study builds on prior research that suggests nudges to consider the truthfulness of content can help reduce the spread of misinformation, but extends this to test whether the same effect applies to deepfakes—a sophisticated form of synthetic media generated by AI.

The experiment is structured to randomly assign participants into two groups: one exposed to the accuracy nudge and one control group without the nudge. The nudge involves a simple prompt asking participants to assess the truthfulness of a neutral news headline. Following this, participants will evaluate a series of four stimuli: two videos (a deepfake of a dog carrying a baby and a real video of a dog with a baby) and two news headlines in thumbnail format (a false and a real headline about mpox). Participants will be asked whether they would share this content via private or public channels and provide comments to gauge belief in the content.

## Repository Structure

```
📁 Non-Harmful Deepfakes Experiment
│
├── 📁 Ethics committee/       # Ethical approval document
├── 📁 Otree app/              # oTree application in Python for survey-experiment
│   ├── 📁 app/                # Main experiment logic and HTML templates
│   │   ├── static/           # Static resources (CSS, images, JavaScript, etc.)
│   │   ├── __init__.py       # Python module initialization
│   │   ├── Consent.html      # Consent form page
│   │   ├── Contact.html      # Contact information page
│   │   ├── Content1-4.html   # Experiment content pages
│   │   ├── Crt.html          # Cognitive Reflection Task
│   │   ├── Decline.html      # Page for participants who decline participation
│   │   ├── Demographics.html # Demographic survey
│   │   ├── Endpage.html      # Final page of the experiment
│   │   ├── Info.html         # Information page about the study
│   │   ├── trtmnt.html       # Accuracy Nudge page
│   ├── db.sqlite3            # Local database for experiment data
│   ├── requirements.txt      # Python dependencies
│   ├── runtime.txt           # Runtime configuration
│   ├── settings.py           # Experiment settings
│   ├── .gitignore            # Files to ignore in version control
│
├── 📁 Stimuli/               # Experimental stimuli (videos and articles)
│   ├── Cute video - Deepfake.mp4   # Deepfake video stimulus
│   ├── Cute video - True.mp4       # Real video stimulus
│   ├── Health related (mpox) - False.png   # False headline stimulus
│   ├── Health related (mpox) - True.png    # True headline stimulus
│   ├── Placebo - True.png          # Control stimulus
│
├── Accuracy nudges on deepfakes - Preregistration.pdf  # Study preregistration document
├── Appendix - Accuracy nudges on deepfakes.pdf        # Additional documentation
├── Deepfakes_stimuli_public.xlsx                      # Questionnaires in English and Spanish
```

## How to Use

1. **Run the oTree App**

   - Install dependencies:
     ```sh
     pip install -r requirements.txt
     ```
   - Run the server:
     ```sh
     otree devserver
     ```
   - Open `http://localhost:8000` to access the experiment.

2. **View Stimuli**

   - The `Stimuli/` folder contains the videos and headlines used in the experiment.

3. **Review Study Materials**

   - The `Deepfakes_stimuli_public.xlsx` file includes the full questionnaire in both English and Spanish.
   - Ethical approval documents are in the `Ethics committee/` folder.

## License
This repository is intended for academic and research purposes, then licensed under the MIT License - see the [LICENSE](LICENSE) file for details. If you use or modify this work, please cite appropriately.
