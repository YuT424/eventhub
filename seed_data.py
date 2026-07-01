"""
Seed script for EventHub - populates the database with sample data.
Run: python seed_data.py
"""
from eventhub import create_app, db
from eventhub.models import User, Event, Comment, Booking, EventStatus
from flask_bcrypt import generate_password_hash
from datetime import datetime, timedelta
import uuid


def seed():
    app = create_app()
    with app.app_context():
        # Clean existing data
        db.drop_all()
        db.create_all()

        # ============================================================
        #  Users
        # ============================================================
        users_data = [
            {
                "first_name": "Sarah",
                "last_name": "Chen",
                "email": "sarah.chen@example.com",
                "password": "password123",
                "phone": "0412 345 678",
                "street_address": "12 Queen Street, Brisbane",
            },
            {
                "first_name": "James",
                "last_name": "Wilson",
                "email": "james.wilson@example.com",
                "password": "password123",
                "phone": "0423 456 789",
                "street_address": "45 Adelaide Street, Brisbane",
            },
            {
                "first_name": "Emma",
                "last_name": "Nguyen",
                "email": "emma.nguyen@example.com",
                "password": "password123",
                "phone": "0434 567 890",
                "street_address": "78 Creek Street, Brisbane",
            },
        ]

        users = []
        for u in users_data:
            pw_hash = generate_password_hash(u.pop("password")).decode("utf-8")
            user = User(password_hash=pw_hash, **u)
            db.session.add(user)
            users.append(user)

        db.session.flush()  # get user IDs
        print(f"Created {len(users)} users")

        # ============================================================
        #  Events (with real images from Pexels)
        # ============================================================
        # Pexels image URL helper
        def pexels(photo_id, ext="jpeg"):
            return f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.{ext}?auto=compress&cs=tinysrgb&w=800&h=500&dpr=1"

        now = datetime.now()

        events_data = [
            # --- Conference ---
            {
                "name": "AI & Future Tech Summit 2026",
                "description": "Join industry leaders and innovators at the AI & Future Tech Summit 2026. This full-day conference features keynote presentations from top AI researchers, hands-on demos of cutting-edge technology, and networking opportunities with startups and established tech companies.\n\nTopics include:\n- Generative AI and its impact on industry\n- Machine Learning at scale\n- Ethics and responsible AI\n- The future of human-AI collaboration\n\nLunch and refreshments included in ticket price.",
                "category": "Conference",
                "date": now + timedelta(days=30),
                "venue": "Brisbane Convention & Exhibition Centre",
                "price": 150.00,
                "total_tickets": 200,
                "available_tickets": 200,
                "status": EventStatus.OPEN,
                "image": pexels(9275222),
                "user_id": users[0].id,
            },
            {
                "name": "Data Analytics Conference",
                "description": "A premier gathering of data scientists, analysts, and business intelligence professionals. Learn about the latest trends in data visualisation, predictive analytics, and big data infrastructure.\n\nFeaturing speakers from leading tech companies and hands-on workshops.",
                "category": "Conference",
                "date": now + timedelta(days=60),
                "venue": "QUT Gardens Point Campus",
                "price": 120.00,
                "total_tickets": 150,
                "available_tickets": 87,
                "status": EventStatus.OPEN,
                "image": pexels(7648043),
                "user_id": users[1].id,
            },
            {
                "name": "Web3 & Blockchain Forum",
                "description": "Explore the decentralised future at our Web3 & Blockchain Forum. Industry experts will discuss blockchain applications, smart contracts, NFTs, and the evolution of decentralised finance.\n\nWhether you're a developer, investor, or curious beginner, this event offers valuable insights into the Web3 ecosystem.",
                "category": "Conference",
                "date": now - timedelta(days=5),
                "venue": "Royal International Convention Centre",
                "price": 95.00,
                "total_tickets": 100,
                "available_tickets": 0,
                "status": EventStatus.INACTIVE,
                "image": pexels(8761738),
                "user_id": users[0].id,
            },
            # --- Workshop ---
            {
                "name": "Python for Beginners Workshop",
                "description": "A hands-on, full-day workshop designed for absolute beginners. Learn the fundamentals of Python programming from scratch.\n\nWhat you'll learn:\n- Variables, data types, and operators\n- Control flow (if/else, loops)\n- Functions and modules\n- File handling\n- Introduction to data analysis with Python\n\nNo prior programming experience required. Bring your own laptop.",
                "category": "Workshop",
                "date": now + timedelta(days=14),
                "venue": "QUT Kelvin Grove Campus, Room KG-E201",
                "price": 45.00,
                "total_tickets": 30,
                "available_tickets": 12,
                "status": EventStatus.OPEN,
                "image": pexels(8761299),
                "user_id": users[1].id,
            },
            {
                "name": "UI/UX Design Masterclass",
                "description": "Elevate your design skills in this intensive masterclass. Learn user-centred design principles, prototyping with Figma, and how to conduct user research that drives product decisions.\n\nPerfect for aspiring designers and developers who want to create better user experiences.",
                "category": "Workshop",
                "date": now + timedelta(days=45),
                "venue": "The Precinct, Fortitude Valley",
                "price": 85.00,
                "total_tickets": 25,
                "available_tickets": 25,
                "status": EventStatus.OPEN,
                "image": pexels(9034869),
                "user_id": users[2].id,
            },
            {
                "name": "Digital Marketing Bootcamp",
                "description": "A comprehensive bootcamp covering SEO, social media marketing, email campaigns, and paid advertising. Learn from real-world case studies and build a marketing strategy during the session.\n\nIncludes templates, checklists, and a certificate of completion.",
                "category": "Workshop",
                "date": now + timedelta(days=21),
                "venue": "Brisbane Innovation Hub",
                "price": 65.00,
                "total_tickets": 40,
                "available_tickets": 40,
                "status": EventStatus.OPEN,
                "image": pexels(8134067),
                "user_id": users[0].id,
            },
            # --- Music ---
            {
                "name": "Brisbane Live Music Festival",
                "description": "Experience an unforgettable evening of live music featuring local and interstate artists across multiple genres. From indie rock to electronic, this festival showcases the best of Brisbane's vibrant music scene.\n\nFood trucks and bars on site. All ages welcome (under 18 must be accompanied by an adult).",
                "category": "Music",
                "date": now + timedelta(days=35),
                "venue": "Riverstage, Brisbane City Botanic Gardens",
                "price": 55.00,
                "total_tickets": 500,
                "available_tickets": 312,
                "status": EventStatus.OPEN,
                "image": pexels(4218027),
                "user_id": users[2].id,
            },
            {
                "name": "Classical Symphony Night",
                "description": "An evening of timeless classical masterpieces performed by the Brisbane Symphony Orchestra. The programme includes works by Beethoven, Mozart, and Tchaikovsky.\n\nDoors open at 6:30 PM. Performance starts at 7:30 PM. Dress code: smart casual.",
                "category": "Music",
                "date": now + timedelta(days=50),
                "venue": "Queensland Performing Arts Centre (QPAC)",
                "price": 75.00,
                "total_tickets": 300,
                "available_tickets": 0,
                "status": EventStatus.SOLD_OUT,
                "image": pexels(167605),
                "user_id": users[1].id,
            },
            {
                "name": "Electronic Dance Party",
                "description": "Dance the night away with top DJs from across Australia. Featuring state-of-the-art sound and lighting systems, this is Brisbane's biggest electronic music event of the year.\n\n18+ only. Valid ID required at entry.",
                "category": "Music",
                "date": now + timedelta(days=70),
                "venue": "The Triffid, Newstead",
                "price": 40.00,
                "total_tickets": 250,
                "available_tickets": 198,
                "status": EventStatus.OPEN,
                "image": pexels(1652361),
                "user_id": users[2].id,
            },
            # --- Sports ---
            {
                "name": "Brisbane City Marathon 2026",
                "description": "Challenge yourself in the annual Brisbane City Marathon! With full marathon (42.2km), half marathon (21.1km), and 10km options, there's a distance for everyone.\n\nAll finishers receive a medal and event t-shirt. Proceeds support local children's charities.\n\nRegistration includes race bib, timing chip, and post-race refreshments.",
                "category": "Sports",
                "date": now + timedelta(days=40),
                "venue": "South Bank Parklands (Start/Finish)",
                "price": 60.00,
                "total_tickets": 1000,
                "available_tickets": 743,
                "status": EventStatus.OPEN,
                "image": pexels(30313133),
                "user_id": users[0].id,
            },
            {
                "name": "Inter-University Basketball Tournament",
                "description": "Watch top university teams compete in an action-packed basketball tournament. Hosted at QUT's state-of-the-art sports facility.\n\nFree entry for students with valid ID. General admission tickets available for the public.",
                "category": "Sports",
                "date": now + timedelta(days=25),
                "venue": "QUT Gardens Point Sports Centre",
                "price": 15.00,
                "total_tickets": 200,
                "available_tickets": 156,
                "status": EventStatus.OPEN,
                "image": pexels(12256528),
                "user_id": users[1].id,
            },
            # --- Social ---
            {
                "name": "Networking Mixer & Tech Startup Showcase",
                "description": "Connect with fellow entrepreneurs, investors, and tech enthusiasts at our monthly networking mixer. This month features a showcase of 5 exciting Brisbane-based startups.\n\nComplimentary drinks and canapes. Limited spots available - register early!\n\nSponsored by Brisbane Innovation Hub and QUT Entrepreneurship.",
                "category": "Social",
                "date": now + timedelta(days=10),
                "venue": "The Precinct, Fortitude Valley",
                "price": 25.00,
                "total_tickets": 80,
                "available_tickets": 34,
                "status": EventStatus.OPEN,
                "image": pexels(8761317),
                "user_id": users[2].id,
            },
            {
                "name": "Charity Gala Dinner",
                "description": "An elegant evening of fine dining, live entertainment, and fundraising for Brisbane Homeless Services. The night features a three-course meal, silent auction, and performances by local artists.\n\nBlack tie dress code. Tables of 10 available at a discounted rate.",
                "category": "Social",
                "date": now + timedelta(days=55),
                "venue": "Hilton Brisbane Hotel",
                "price": 120.00,
                "total_tickets": 120,
                "available_tickets": 67,
                "status": EventStatus.OPEN,
                "image": pexels(16385072),
                "user_id": users[0].id,
            },
            # --- Cancelled event ---
            {
                "name": "Outdoor Film Festival",
                "description": "An outdoor cinema experience under the stars, featuring classic and contemporary films. Unfortunately, this event has been cancelled due to unforeseen circumstances. Refunds will be processed automatically.",
                "category": "Social",
                "date": now + timedelta(days=20),
                "venue": "Roma Street Parkland",
                "price": 20.00,
                "total_tickets": 150,
                "available_tickets": 150,
                "status": EventStatus.CANCELLED,
                "image": pexels(1708936),
                "user_id": users[1].id,
            },
        ]

        events = []
        for ed in events_data:
            event = Event(**ed)
            db.session.add(event)
            events.append(event)

        db.session.flush()
        print(f"Created {len(events)} events")

        # ============================================================
        #  Comments
        # ============================================================
        comments_data = [
            (events[0], users[1], "Looking forward to the AI Summit! The speaker lineup looks amazing."),
            (events[0], users[2], "Is there a student discount available? Would love to attend!"),
            (events[0], users[0], "Hi Emma, yes there's a 20% student discount. Use code STUDENT20 at checkout."),
            (events[3], users[0], "Perfect timing! I've been wanting to learn Python. Just registered!"),
            (events[3], users[2], "Do we need to install Python before the workshop?"),
            (events[3], users[1], "Hi Emma, yes please install Python 3.12 from python.org. We'll send a setup guide via email."),
            (events[6], users[0], "The lineup is incredible! Can't wait for this."),
            (events[6], users[1], "Are food trucks vegan-friendly?"),
            (events[6], users[2], "Yes! There are several vegan options available. See you there!"),
            (events[7], users[0], "Disappointed it's sold out. Will there be a waitlist?"),
            (events[7], users[2], "Same! I really wanted to see the Beethoven piece."),
            (events[9], users[2], "Training for the half marathon. This is going to be great!"),
            (events[9], users[1], "The route along the river is beautiful. Highly recommend!"),
            (events[11], users[1], "Great opportunity to meet other founders. Last month's mixer was fantastic."),
            (events[13], users[2], "Such a shame it's cancelled. Was really looking forward to it."),
        ]

        for event, user, content in comments_data:
            comment = Comment(
                content=content,
                user_id=user.id,
                event_id=event.id,
                created_at=now - timedelta(hours=hash(content) % 72),
            )
            db.session.add(comment)

        print(f"Created {len(comments_data)} comments")

        # ============================================================
        #  Bookings
        # ============================================================
        bookings_data = [
            (events[0], users[1], 2),
            (events[0], users[2], 1),
            (events[3], users[0], 1),
            (events[3], users[2], 1),
            (events[6], users[0], 3),
            (events[6], users[1], 2),
            (events[7], users[0], 2),
            (events[7], users[1], 1),
            (events[9], users[2], 1),
            (events[11], users[1], 2),
            (events[12], users[0], 1),
        ]

        for event, user, qty in bookings_data:
            booking = Booking(
                order_id=str(uuid.uuid4()),
                quantity=qty,
                total_price=event.price * qty,
                booking_date=now - timedelta(days=hash(str(event.id) + str(user.id)) % 10),
                user_id=user.id,
                event_id=event.id,
            )
            db.session.add(booking)

        print(f"Created {len(bookings_data)} bookings")

        db.session.commit()
        print("\n=== Database seeded successfully! ===")
        print(f"  Users:    {len(users)}")
        print(f"  Events:   {len(events)}")
        print(f"  Comments: {len(comments_data)}")
        print(f"  Bookings: {len(bookings_data)}")
        print("\nLogin credentials for testing:")
        print("  sarah.chen@example.com / password123")
        print("  james.wilson@example.com / password123")
        print("  emma.nguyen@example.com / password123")


if __name__ == "__main__":
    seed()
