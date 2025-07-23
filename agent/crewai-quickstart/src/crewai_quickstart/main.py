#!/usr/bin/env python
# src/crewai-quickstart/main.py
import sys
from crewai_quickstart.crew import LatestAiDevelopmentCrew

def run():
  """
  Run the crew.
  """
  inputs = {
    'topic': 'AI Agents'
  }
  LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)