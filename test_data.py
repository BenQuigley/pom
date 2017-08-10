from app.models import User, Poem

def initialize_db():
    navigate = "What tempestuous destiny rushes at them\n" \
               "Who captain their lives, with honor flying as standards,\n" \
               "But with minds as holds, full of millions of worms?\n" \
               "Their houses are full of boxes never unpacked from the move,\n" \
               "That nation of plagiarists,\n" \
               "And the gray glow of computers as they read in bed\n" \
               "Is finally painting their own blue and brown eyes gray.\n" \
               "The indifference of the trees to their ennui,\n" \
               "The swagger of their overfed cats,\n" \
               "The thoughtlessness of what is rotting on the road...\n" \
               "It can swallow a generation; we just know this.\n" \
               "That is its breath they smell when they are microwaving dinner.\n" \
               "Later over the speakers the iPod shuffle-stumbles\n" \
               "To a Segovia waltz or an old song\n" \
               "Their mothers used to sing, as they twist\n" \
               "In the bed sheets together – recalling\n" \
               "The Polaroid memories of their childhoods, but reflecting\n" \
               "How the film for a Polaroid just isn't made anymore."
    user = User(nickname="iroh", password='meow', email='benquigleyconsulting@gmail.com')
    poem = Poem(name="They Navigate by Constellation", body=navigate, user_id=user.id)

    db.create_all()
    db.session.add(user)
    db.session.add(poem)
    db.session.commit()