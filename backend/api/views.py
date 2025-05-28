from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
import torch
from dotenv import load_dotenv
import os

load_dotenv()

# Use GPU if available
device = 0 if torch.cuda.is_available() else -1

# Load models once
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")
email_writer = pipeline("text2text-generation", model="google/flan-t5-large")

class SummarizeView(APIView):
    def post(self, request):
        notes = request.data.get("notes")
        if not notes:
            return Response({"error": "Missing notes"}, status=status.HTTP_400_BAD_REQUEST)

        summary = summarizer(notes, max_length=350, min_length=100, do_sample=True, temperature=0.7)
        summary_text = summary[0]["summary_text"]
        return Response({"summary": summary_text})

class EmailView(APIView):
    def post(self, request):
        summary = request.data.get("summary")
        if not summary:
            return Response({"error": "Missing summary"}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""
        Write a professional follow-up email based on the meeting summary below.
        The email should:
        - Include a subject line with client's business name and 'follow up'
        - Recap the client's goals and pain points
        - Highlight any deadlines or budget considerations
        - Clearly list next steps and responsible parties

        Meeting Summary:
        {summary}
        """
        email = email_writer(prompt, max_length=500, min_length=100, do_sample=True, temperature=0.6)
        return Response({"email": email[0]['generated_text']})
