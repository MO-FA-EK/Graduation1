
import os
import django
import random
from faker import Faker

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Programmer, Project

fake = Faker()

CATEGORIES = ['Web Development', 'Data Science', 'Mobile Dev', 'Cyber Security', 'UI/UX Design']
SKILLS_LIST = ['Python', 'Django', 'Angular', 'React', 'Node.js', 'SQL', 'AWS', 'Docker', 'Machine Learning', 'Java', 'Swift', 'Kotlin']

def create_freelancers(n=15):
    print(f"Creating {n} freelancers...")
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = 'password123'
        
        if User.objects.filter(username=username).exists():
            continue

        user = User.objects.create_user(username=username, email=email, password=password)
        
        category = random.choice(CATEGORIES)
        skills = ", ".join(random.sample(SKILLS_LIST, k=random.randint(3, 6)))
        
        Programmer.objects.create(
            user=user,
            name=fake.name(),
            category=category,
            skills=skills,
            experience_level=random.choice(['Junior', 'Mid-Level', 'Senior']),
            bio=fake.text(max_nb_chars=200),
            hourly_rate=random.randint(20, 150),
            image_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}",
            review_count=random.randint(0, 50),
            rating=round(random.uniform(3.5, 5.0), 1),
            profile_views=random.randint(10, 500)
        )
    print("Done creating freelancers.")

def create_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created with password 'admin123'")
    else:
        print("Superuser 'admin' already exists.")

if __name__ == '__main__':
    create_admin()
    create_freelancers(20)
