from django.shortcuts import render


def index(request):
    context = {
        'benefits': [
            {
                'icon': '🚀',
                'title': 'Claude Pro Access',
                'description': 'Free unlimited access to Claude\'s most advanced models with priority processing. Build, research, and create without limits.',
            },
            {
                'icon': '💻',
                'title': '$50/mo API Credits',
                'description': 'Monthly API credits to build real applications powered by Claude. Ship projects, automate workflows, and experiment freely.',
            },
            {
                'icon': '🎓',
                'title': 'Workshops & Hackathons',
                'description': 'Hands-on workshops, weekend hackathons, and demo nights. Learn prompt engineering, AI app development, and more.',
            },
            {
                'icon': '🤝',
                'title': 'Community & Networking',
                'description': 'Connect with fellow builders across all majors. Guest speakers from Anthropic and industry leaders share insights.',
            },
        ],
        'gallery': [
            {'caption': 'First club presentation', 'image': 'landing/images/gallery/1.jpg'},
            {'caption': 'Workshop: Intro to Claude Code', 'image': 'landing/images/gallery/2.jpg'},
            {'caption': 'Claude Builder Club & Robotics', 'image': 'landing/images/gallery/3.jpg'},
            {'caption': 'Claude Builder Outreach', 'image': 'landing/images/gallery/4.jpg'},
        ],
        'stats': [
            {'value': '60+', 'num': 60, 'label': 'Universities Nationwide'},
            {'value': '15K+', 'num': 15000, 'label': 'Student Builders'},
            {'value': '7', 'num': 7, 'label': 'Ivy League Schools'},
            {'value': '∞', 'num': 0, 'label': 'Projects to Build'},
        ],
        'events': [
            {
                'month': 'Mar',
                'day': '8',
                'year': 2026,
                'month_num': 3,
                'day_num': 8,
                'title': 'Kickoff Meeting & Info Session',
                'description': 'Learn about CBC Mizzou, meet the team, and get set up with Claude Pro access. Pizza provided!',
                'location': 'Lafferre Hall, Room 100',
                'time': '2:00 PM – 3:30 PM',
            },
            {
                'month': 'Mar',
                'day': '15',
                'year': 2026,
                'month_num': 3,
                'day_num': 15,
                'title': 'Workshop: Building with the Claude API',
                'description': 'Hands-on workshop covering API basics, prompt engineering, and building your first AI-powered app.',
                'location': 'Engineering Building West, Lab 204',
                'time': '1:00 PM – 4:00 PM',
            },
            {
                'month': 'Mar',
                'day': '29',
                'year': 2026,
                'month_num': 3,
                'day_num': 29,
                'title': 'AI Hackathon: Build Something Cool',
                'description': '12-hour hackathon to build AI projects with Claude. Prizes for best app, most creative use, and best pitch.',
                'location': 'Student Center, Stotler Lounge',
                'time': '9:00 AM – 9:00 PM',
            },
            {
                'month': 'Apr',
                'day': '12',
                'year': 2026,
                'month_num': 4,
                'day_num': 12,
                'title': 'Demo Night & Guest Speaker',
                'description': 'Show off what you\'ve built and hear from an Anthropic engineer about the future of AI development.',
                'location': 'Memorial Union, Wrench Auditorium',
                'time': '5:00 PM – 7:30 PM',
            },
        ],
        'team': [
            {'name': 'Brandon Gomes', 'initials': 'BG', 'role': 'President', 'major': 'BS in Computer Science & Math, Senior', 'linkedin': 'https://www.linkedin.com/in/brandon-gomes-mu/', 'image': 'landing/images/team/brandon.jpeg'},
            {'name': 'Pari Patel', 'initials': 'PP', 'role': 'Vice President', 'major': 'BS in Computer Science, Senior', 'linkedin': 'https://www.linkedin.com/in/paripatel54/', 'image': 'landing/images/team/pari.jpeg'},
            {'name': 'Colton Treloar', 'initials': 'CT', 'role': 'Treasurer', 'major': 'Computer Science, Junior', 'linkedin': 'https://www.linkedin.com/in/colton-treloar-613442206/', 'image': 'landing/images/team/colton.jpg'},
            {'name': 'Akbar K.', 'initials': 'AK', 'role': 'Secretary', 'major': 'BS in Electrical Engineering, Junior', 'linkedin': 'https://www.linkedin.com/in/akbarjon-kamoldinov/', 'image': 'landing/images/team/akbar.jpeg'},
            {'name': 'Sebastian Main', 'initials': 'SM', 'role': 'Outreach', 'major': 'Information Technology, Junior', 'linkedin': 'https://www.linkedin.com/in/sebastian-main-6a4799224/', 'image': 'landing/images/team/sebastian.jpg'},
        ],
        'projects': [
            {
                'title': 'PromptVault',
                'description': 'A community-driven platform for discovering and sharing the best AI prompts for Claude, ChatGPT, Gemini, and more. Browse trending prompts by category, like and share with fellow prompt engineers.',
                'tech': ['Next.js', 'Supabase', 'Tailwind CSS'],
                'link': 'https://promptvaultt.netlify.app/',
            },
            {
                'title': 'MizzouMeal Planner',
                'description': 'AI-powered meal planning app that creates personalized weekly plans based on dining hall menus and dietary preferences.',
                'tech': ['Claude API', 'Next.js', 'Supabase'],
                'coming_soon': True,
            },
            {
                'title': 'StudyBuddy AI',
                'description': 'Upload your lecture notes and get auto-generated flashcards, practice quizzes, and study guides powered by Claude.',
                'tech': ['Claude API', 'React', 'Firebase'],
                'coming_soon': True,
            },
        ],
        'faq_items': [
            {
                'question': 'Who can join CBC Mizzou?',
                'answer': 'Any currently enrolled Mizzou student can join, regardless of major or coding experience. We welcome engineers, journalists, business students, artists — anyone interested in building with AI.',
            },
            {
                'question': 'Do I need coding experience?',
                'answer': "Not at all! We have tracks for all skill levels. Our workshops start from the basics, and Claude itself is a great tool for learning to code. Many of our most creative projects come from non-CS majors.",
            },
            {
                'question': 'How do I get free Claude Pro access?',
                'answer': "Join the club by filling out our sign-up form. Once you're a member, you'll receive instructions to activate your free Claude Pro subscription within a few days.",
            },
            {
                'question': "What's the time commitment?",
                'answer': "Totally flexible. We host events 2-3 times per month, and attendance is optional. Come to what interests you — whether that's every workshop or just the hackathons.",
            },
            {
                'question': 'How are the $50 monthly API credits distributed?',
                'answer': "Active members receive API credits through Anthropic's program. You'll get access to the Claude API to build personal projects, class assignments, or hackathon submissions.",
            },
            {
                'question': 'Can I join the leadership team?',
                'answer': "Yes! We're always looking for motivated students to help lead workshops, organize events, manage social media, and grow the community. Reach out to any current leader to learn more.",
            },
            {
                'question': 'Where do meetings take place?',
                'answer': 'We rotate between rooms in Lafferre Hall, the Engineering Building, and the Student Center. Check our GroupMe and events calendar for specific locations each week.',
            },
        ],
        'links': {
            'groupme': 'https://groupme.com/join_group/112902855/DrXZJmkl',
            'instagram': 'https://www.instagram.com/claude.miz/',
            'linkedin': 'https://www.linkedin.com/groups/18313009/',
            'email': 'mailto:cbcmizzou@gmail.com',
            'signup': 'https://forms.gle/K6WxeEaavtafNjAP7',
            'claude_ai': 'https://claude.ai',
            'anthropic': 'https://anthropic.com',
            'api_docs': 'https://docs.anthropic.com',
        },
    }
    return render(request, 'landing/index.html', context)