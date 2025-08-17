from django.db import models

class Resume(models.Model):
    resume_file = models.FileField(upload_to="resumes/")
    analysis_result = models.TextField(blank=True, null=True)  # Stores JSON analysis results
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} uploaded on {self.uploaded_at}"

