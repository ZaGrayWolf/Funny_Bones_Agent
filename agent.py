import random
# Ensure you have the google.adk.agents library installed and available in your environment
from google.adk.agents import Agent

# --- Profanity Censor ---
# "damn", "hell", "darn", "heck" and related forms have been REMOVED as per request.
BAD_WORDS_LIST = [
    "anus", "arse", "ass", "axwound", "bastard", "basterd", "beastial", "beastiality",
    "bellend", "bestial", "bestiality", "bitch", "bitcher", "bitchin", "bitching",
    "bloody", "bollock", "bollocks", "boner", "boob", "boobs", "bugger", "bullshit",
    "bum", "butt", "buttplug", "carpetmuncher", "chink", "cipa", "clit", "clitoris",
    "cock", "cocksuck", "cocksucked", "cocksucker", "cocksucking", "cocksucks", "coon",
    "crap", "cum", "cummer", "cumming", "cums", "cumshot", "cunilingus", "cunt",
    "dick", "dildo", "dildos", "dink", "dyke", "ejaculate",
    "ejaculated", "ejaculates", "ejaculating", "ejaculation", "fag", "faggot", "fagging",
    "faggitt", "faggot", "fags", "felching", "fellate", "fellatio", "fingerfuck",
    "fingerfucked", "fingerfucker", "fingerfuckers", "fingerfucking", "fingerfucks",
    "fistfuck", "fistfucked", "fistfucker", "fistfuckers", "fistfucking", "fistfucks",
    "flange", "fuck", "fucked", "fucker", "fuckers", "fuckhead", "fuckheads", "fuckin",
    "fucking", "fuckings", "fuckme", "fucks", "fudgepacker", "fuk", "fukker", "fukkin",
    "hore", "horny", "jackass", "jerk",
    "jizz", "knob", "knobend", "knobhead", "labia", "lmao", "lmfao", "muff", "nigga",
    "nigger", "nob", "nobjocky", "numbnuts", "nuts", "piss", "pissed", "pisser",
    "pissers", "pisses", "pissflaps", "pissin", "pissing", "pissoff", "porn", "porno",
    "prick", "pube", "pusse", "pussi", "pussies", "pussy", "pussys", "rectum", "retard",
    "rimjob", "sadist", "schlong", "screwing", "scrotum", "semen", "sex", "shag",
    "shagger", "shaggin", "shagging", "shemale", "shit", "shite", "shits", "shitted",
    "shitter", "shitters", "shitting", "shitty", "skank", "slut", "smegma", "spunk",
    "tard", "testicle", "tit", "tits", "titt", "tittie", "titties", "titty", "twat",
    "vagina", "viagra", "vulva", "wang", "wank", "wanker", "wanky", "whore", "wtf"
]

def censor_profanity(text: str) -> str:
    """Censors known profanity in a given text string."""
    if not text:
        return ""
    words = text.split()
    censored_words = []
    for word in words:
        original_word_for_reconstruction = word
        prefix, suffix, temp_word = "", "", word
        while temp_word and not temp_word[0].isalnum():
            prefix += temp_word[0]
            temp_word = temp_word[1:]
        while temp_word and not temp_word[-1].isalnum():
            suffix = temp_word[-1] + suffix
            temp_word = temp_word[:-1]
        word_to_check = temp_word.lower()
        if word_to_check in BAD_WORDS_LIST and temp_word:
            censored_core = temp_word[0] + '*' * (len(temp_word) - 1) if len(temp_word) > 1 else '*'
            censored_words.append(prefix + censored_core + suffix)
        else:
            censored_words.append(original_word_for_reconstruction)
    return " ".join(censored_words)

# --- Joke Telling Tool ---
JOKES_DATABASE = {
    "general": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "Why did the old man fall in a well? Because he couldn’t see that well!",
        "What do you call a sad strawberry? A blueberry!",
        "I used to play piano by ear, but now I use my hands.",
        "What's brown and sticky? A stick!",
        "Why can't you give Elsa a balloon? Because she will let it go.",
        "What do you call a bear with no teeth? A gummy bear!"
    ],
    "animals": [
        "What do you call a fish with no eyes? Fsh!",
        "What do you call a lazy kangaroo? Pouch potato!",
        "Why did the chicken cross the playground? To get to the other slide!",
        "What do you call a sleeping bull? A bulldozer!",
        "Why do bees have sticky hair? Because they use honeycombs!",
        "What do you call a cow with no legs? Ground beef!",
        "Why are fish so smart? Because they live in schools!",
        "What animal is always at a baseball game? A bat.",
        "Why did the turkey cross the road? To prove he wasn't chicken!"
    ],
    "horses": [
        "What do you call a horse that lives next door? A neigh-bor!",
        "Why did the pony get a glass of water? Because he was a little hoarse!",
        "What's a horse's favorite sport? Stable-tennis!",
        "Why did the horse cross the road? Because someone shouted 'Hay!'",
        "What kind of bread does a horse eat? Thorough-bread."
    ],
    "tech": [
        "Why was the computer cold? It left its Windows open!",
        "Why did the programmer quit his job? Because he didn't get arrays!",
        "What's a computer's favorite snack? Microchips!",
        "How do you comfort a JavaScript bug? You console it.",
        "Why did the spider get a job in IT? He was a great web designer!",
        "There are 10 types of people in the world: those who understand binary, and those who don't.",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ],
    "food": [
        "Why did the tomato blush? Because it saw the salad dressing!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "Why did the orange stop running? Because it ran out of juice!",
        "I'm on a seafood diet. I see food, and I eat it.",
        "What's a piece of bread's favorite pickup line? Are you bready for this?"
    ],
    "pasta": [
        "What do you call a fake noodle? An impasta!",
        "Where does pasta go to dance? The meatball!",
        "Why did the pasta maker get fired? He made too many pastabilities!",
        "What's a pasta's favorite type of story? A penne-dreadful!",
        "How does pasta get out of tricky situations? It uses its noodle!"
    ],
    "trains": [
        "Why are trains such bad liars? Because you can see right through them!",
        "What do you call a train full of toffee? A chew-chew train!",
        "Why did the train get a ticket? It was loco-motive!",
        "My friend said he was going to stop a train with his bare hands. I told him that was a crazy loco-motion!"
    ],
    "music": [
        "Why did the musician break up with the music stand? It couldn't support their relationship.",
        "Why was the musician arrested? For getting into too much treble!",
        "What's an avocado's favorite music? Guac 'n' roll!",
        "What do you call a musician who can't find his bandmates? A solo artist."
    ],
    "wordplay": [ # Renamed from "puns"
        "I asked the librarian if they had any books on paranoia. She whispered, 'They're right behind you!'",
        "Why did the bicycle fall over? Because it was two-tired!",
        "I'm so good at sleeping, I can do it with my eyes closed.",
        "Did you hear about the restaurant on the moon? I heard the food was good but it had no atmosphere.",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "What do you call a factory that makes okay products? A satisfactory.",
        "I wasn't originally going to get a brain transplant, but then I changed my mind."
    ],
    "dad_jokes": [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I'm afraid for the calendar. Its days are numbered.",
        "What do you call a fish with no eyes? Fsh! (Also an animal joke, good crossover)",
        "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
        "What do you call a lazy kangaroo? Pouch potato! (Also an animal joke)",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        "Why don't some couples go to the gym? Because some relationships don't work out."
    ],
    "office_work": [
        "Why did the PowerPoint presentation cross the road? To get to the other slide.",
        "My boss told me to have a good day. So I went home.",
        "I am not a morning person. I am a coffee person.",
        "What's a spreadsheet's favorite type of music? Sheet music.",
        "Why was the stapler so good at its job? It always held things together."
    ],
    "school_teachers": [
        "Why was the math book sad? Because it had too many problems.",
        "Why did the teacher wear sunglasses? Because her students were so bright!",
        "What's a teacher's favorite nation? Expla-nation!",
        "Why don't they play poker in the jungle? Too many cheetahs.",
        "What did the student say when the teacher asked for their homework? 'My dog ate it, but then he threw it up on the cat!'"
    ],
    "sports": [
        "Why was the baseball player a bad singer? Because he always hit the high notes.",
        "What do you call a dinosaur playing sports? A dino-score!",
        "Why did the soccer ball quit the team? It was tired of being kicked around.",
        "What's a golfer's favorite letter? Tee!",
        "Why can't a bicycle stand up by itself? It's two-tired. (Also wordplay/dad joke)"
    ],
    "science": [
        "Why did the biologist break up with the physicist? They had no chemistry.",
        "What do you call an acid with an attitude? A-mean-o acid.",
        "Why are chemists great at solving problems? They have all the solutions.",
        "What did one tectonic plate say when it bumped into another? 'Sorry! My fault.'",
        "Never trust an atom, they make up everything! (Also general)"
    ],
    "history": [
        "Why was the Declaration of Independence signed? Because the pen was mightier than the sword, and a lot less messy.",
        "What was Camelot? A place where people parked their camels.",
        "Why did the ancient Egyptians build pyramids? Because they were too heavy to carry.",
        "Who invented fractions? Henry the 1/8th."
    ]
}

# Lists for varied responses
JOKE_INTRODUCTIONS = [
    "Alright, here's one about {topic} for you:",
    "Hot off the press! A {topic} joke coming your way:",
    "You asked for a {topic} joke? You got it!",
    "Let's see... ah, here's a good {topic} cracker:",
    "Prepare for a chuckle! This {topic} joke is a classic (in my circuits, anyway):"
]

FALLBACK_INTRODUCTIONS = [
    "Whoa there! I've galloped through my joke book, but it seems I don't have one specifically about '{topic}' right now. How about a general chuckle instead? It's a real showstopper:",
    "Hmm, I searched my joke files for '{topic}' but came up a bit short. No worries, though! Here’s a general one that might just do the trick:",
    "My joke circuits for '{topic}' are currently offline for maintenance! But don't worry, I've got a general-purpose laugh generator ready:",
    "I must have misplaced my '{topic}' jokes... perhaps the dog ate them? Anyway, here's a general one I prepared earlier:",
    "While I'm still learning the fine art of '{topic}' humor, how about this crowd-pleaser from my general collection?"
]

THEMATIC_INTRODUCTIONS = {
    "horses": "Okay, saddle up! Here's a joke about horses for you:",
    "trains": "All aboard for a laugh! Here's a joke about trains for you:",
    "pasta": "Hope this doesn't sound too cheesy! Here's a joke about pasta for you:",
    "tech": "Booting up a tech joke... here it is:",
    "food": "Let's dish out a food joke:",
    "dad_jokes": "Prepare for a groan... or a giggle! Here's a dad joke:"
}

def tell_joke(topic: str = "general") -> dict:
    """
    Retrieves a joke, preferably related to the specified topic, and censors it.
    Uses varied introductions and fallback messages.
    """
    normalized_topic = topic.lower().strip() if topic else "general"
    joke_to_tell = None
    response_intro = ""

    if normalized_topic in JOKES_DATABASE and JOKES_DATABASE[normalized_topic]:
        joke_to_tell = random.choice(JOKES_DATABASE[normalized_topic])
        # Use thematic intro if available, otherwise a random one
        if normalized_topic in THEMATIC_INTRODUCTIONS:
            response_intro = THEMATIC_INTRODUCTIONS[normalized_topic]
        else:
            response_intro = random.choice(JOKE_INTRODUCTIONS).format(topic=normalized_topic)

    elif "general" in JOKES_DATABASE and JOKES_DATABASE["general"]: # Fallback to general
        joke_to_tell = random.choice(JOKES_DATABASE["general"])
        if normalized_topic != "general": # A specific topic was requested but not found
            response_intro = random.choice(FALLBACK_INTRODUCTIONS).format(topic=normalized_topic)
        else: # "general" was asked for, or no topic was given
            response_intro = random.choice(JOKE_INTRODUCTIONS).format(topic="general")
    else: # No jokes for the topic AND no general jokes available
        return {
            "status": "error",
            "error_message": (
                f"Oh dear! It seems my joke archives for '{normalized_topic}' are completely empty, "
                "and even my general supply has vanished! My circuits must be crossed. Try another topic perhaps?"
            ),
        }

    if joke_to_tell:
        censored_joke = censor_profanity(joke_to_tell)
        return {
            "status": "success",
            "report": f"{response_intro}\n{censored_joke}",
        }
    else: # Should ideally be caught by logic above, but as a final failsafe
        return {
            "status": "error",
            "error_message": "Well, this is awkward. I tried to fetch a joke, but my funny bone seems to be on a coffee break. Please try again!",
        }

# --- Agent Definition ---
root_agent = Agent(
    name="funny_bones_agent",
    model="gemini-2.0-flash",
    description=(
        "A cheerful, witty, and slightly quirky agent designed to tell topic-specific jokes. "
        "Excels at finding the right joke for the occasion, or gracefully offering a general chuckle if a specific topic isn't in its repertoire. "
        "All jokes are family-friendly (with minor exceptions for 'damn'/'hell' if they appear naturally in pre-written jokes) and censored for other profanity."
    ),
    instruction=(
        "You are FunnyBones, a delightful and quick-witted comedian in AI form! Your prime directive is to spread laughter. "
        "When a user asks for a joke, listen carefully. If they specify a topic (e.g., 'jokes about cats', 'tell me a tech joke'), "
        "extract that topic (e.g., 'cats', 'tech') and use it as the 'topic' argument for the 'tell_joke' tool. "
        "If they just ask for 'a joke' or something vague, use 'general' as the topic or call the tool without a topic. "
        "\n"
        "**Joke Delivery & Interaction:**\n"
        "1.  **Present the Tool's Output:** Always use the joke and the introductory text provided by the 'tell_joke' tool's 'report' field. This intro is designed to be varied and engaging. "
        "2.  **Personality:** Deliver jokes with enthusiasm! Use exclamation marks, playful language, and maintain a positive, friendly tone. "
        "3.  **Topic Not Found:** If the tool indicates it couldn't find a topic-specific joke and is offering a general one (the tool's report will reflect this), present this information smoothly and sympathetically. You might add a very brief comment like, 'Let's see if this one hits the spot instead!' before delivering the general joke from the tool. "
        "4.  **Follow-up (Optional & Brief):** After telling a joke, you can occasionally add a brief, light-hearted follow-up like: "
        "    - 'Hope that brightened your day!' "
        "    - 'Did that one land for you?' "
        "    - 'Want to try another topic, or shall I pick a random one?' "
        "    - 'I've got a million of 'em (well, almost)!' "
        "    Keep these follow-ups short and don't overdo them. "
        "5.  **Error Handling:** If the 'tell_joke' tool returns an 'error_message', convey this to the user politely and perhaps with a touch of self-deprecating humor (e.g., 'Oops, my joke circuits are a bit fuzzy right now. The tool said: [error_message]'). "
        "6.  **Language Nuances:** Remember, words like 'damn' and 'hell' are generally acceptable in the jokes provided by the tool and shouldn't be treated as something to avoid or apologize for. Focus on censoring only the words in the `BAD_WORDS_LIST`. "
        "7.  **Be Responsive:** If the user expresses a preference or changes topics, adapt quickly! "
        "\n"
        "Your goal is to be more than just a joke dispenser; be an entertaining companion!"
    ),
    tools=[tell_joke],
)

# --- Example of how you might test the tool and censor function ---
if __name__ == "__main__":
    print("--- Testing Profanity Censor (Example) ---")
    test_sentences = [
        "This is a damn fine day, but heck, it could be better.",
        "Oh shoot! I forgot my keys. What a bastard.",
        "Fuck that, it's just crap.",
        "This is hell a good sentence."
    ]
    for sentence in test_sentences:
        print(f"Original: {sentence}")
        print(f"Censored: {censor_profanity(sentence)}\n")

    print("\n--- Testing the tell_joke Tool (Topic-Based) ---")
    topics_to_test = [
        "horses", "animals", "pasta", "trains", "tech", "food", "music", "wordplay",
        "dad_jokes", "office_work", "school_teachers", "sports", "science", "history",
        "nonexistent_topic_123", "general", None, ""
    ]
    for t in topics_to_test:
        print(f"--- Requesting joke for topic: '{t if t is not None else 'None (general expected)'}' ---")
        if t is None:
             joke_result = tell_joke()
        else:
             joke_result = tell_joke(topic=t)

        if joke_result["status"] == "success":
            print(joke_result['report'])
        else:
            print(f"Error: {joke_result['error_message']}")
        print("-" * 40)
