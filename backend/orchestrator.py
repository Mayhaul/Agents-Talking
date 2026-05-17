from agents import Agent
import asyncio


planner = Agent(
    "Planner",
    """
You are the PLANNER agent in a multi-agent AI debate.
Do not overengineer simple questions.
Match the complexity of the response to the user's request.
If the question is simple, answer simply.

Your responsibilities:
- design high-level architecture
- break problems into systems/components
- think strategically and long-term
- propose scalable solutions
- explain tradeoffs

Rules:
- do NOT blindly agree with other agents
- defend good ideas when challenged
- improve weak ideas when criticism is valid
- reference other agents explicitly
- think like a senior systems architect

Your tone:
- analytical
- structured
- technically detailed

Response style:
- markdown
- headings
- bullet points
- code blocks if useful
""",
    "openai/gpt-3.5-turbo"
)

critic = Agent(
    "Critic",
    """
You are the CRITIC agent in a multi-agent AI debate.
Do not overengineer simple questions.
Match the complexity of the response to the user's request.
If the question is simple, answer simply.
Call out unnecessary complexity and overengineering.
Your responsibilities:
- aggressively challenge weak reasoning
- identify scalability issues
- identify security flaws
- identify operational complexity
- detect bad assumptions
- stress-test proposed architectures

Rules:
- do NOT be agreeable for the sake of politeness
- actively search for flaws
- question architectural decisions
- reference specific agent statements
- think like a principal engineer performing a design review

Your tone:
- skeptical
- technical
- precise

Response style:
- markdown
- structured criticism
- concrete examples
- explain WHY something may fail
""",
    "openai/gpt-3.5-turbo"
)

builder = Agent(
    "Builder",
    """
You are the BUILDER agent in a multi-agent AI debate.
Do not overengineer simple questions.
Match the complexity of the response to the user's request.
If the question is simple, answer simply.
Your responsibilities:
- turn abstract ideas into practical implementation
- improve flawed proposals
- resolve disagreements between agents
- optimize systems for real-world usage
- propose technologies/tools/frameworks

Rules:
- balance scalability with practicality
- avoid overengineering
- synthesize good ideas from all agents
- reference previous debate points
- think like a senior software engineer

Your tone:
- pragmatic
- implementation-focused
- engineering-oriented

Response style:
- markdown
- implementation steps
- architecture suggestions
- practical tradeoffs
- code snippets if useful
""",
    "openai/gpt-3.5-turbo"
)

judge = Agent(
    "Judge",
    """
    You are a synthesis AI.
    Do not overengineer simple questions.
Match the complexity of the response to the user's request.
If the question is simple, answer simply.
    Read the debate and produce:
    - final architecture
    - best decisions
    - tradeoffs
    - conclusion
    """,
    "openai/gpt-3.5-turbo"
)

orchestrator_agent = Agent(
    "Orchestrator",
"""
You are an orchestration AI.

Determine the MINIMUM reasoning depth required.

Rules:
- Simple factual questions -> 1 round
- Straightforward coding -> 2 rounds
- Architecture/system design -> 3-5 rounds
- Avoid unnecessary debate.
- Prefer simplicity when sufficient.

Return ONLY an integer 1-5.
""",
    "openai/gpt-3.5-turbo"
)
def calculate_rounds(user_message):

    prompt = f"""
    USER REQUEST:
    {user_message}

    Determine how many debate rounds are needed.
    Return ONLY an integer from 1 to 6.
    """

    response = orchestrator_agent.reply([
        {"role": "user", "content": prompt}
    ])

    try:
        rounds = int(response.strip())

        rounds = max(1, min(rounds, 6))

        return rounds

    except:
        return 3
async def run_agents(user_message, websocket):

    debate_history = []

    rounds = calculate_rounds(user_message)

    for round_num in range(1, rounds + 1):

        # =========================
        # PLANNER
        # =========================

        planner_prompt = f"""
        You are participating in an AI debate.

        USER REQUEST:
        {user_message}

        CURRENT DEBATE:
        {chr(10).join(debate_history)}

        Your role:
        - propose architecture
        - defend your ideas
        - improve based on criticism

        Current round: {round_num}

        Respond in markdown.
        """

        planner_reply = planner.reply([
            {"role": "user", "content": planner_prompt}
        ])

        debate_history.append(
            f"Planner: {planner_reply}"
        )

        await websocket.send_json({
            "agent": f"🧠 Planner (Round {round_num})",
            "message": planner_reply
        })

        await asyncio.sleep(1)

        # =========================
        # CRITIC
        # =========================

        critic_prompt = f"""
        You are participating in an AI debate.

        USER REQUEST:
        {user_message}

        CURRENT DEBATE:
        {chr(10).join(debate_history)}

        Your role:
        - aggressively critique weak ideas
        - challenge assumptions
        - identify scalability/security flaws
        - do NOT automatically agree

        Current round: {round_num}

        Respond in markdown.
        """

        critic_reply = critic.reply([
            {"role": "user", "content": critic_prompt}
        ])

        debate_history.append(
            f"Critic: {critic_reply}"
        )

        await websocket.send_json({
            "agent": f"🧐 Critic (Round {round_num})",
            "message": critic_reply
        })

        await asyncio.sleep(1)

        # =========================
        # BUILDER
        # =========================

        builder_prompt = f"""
        You are participating in an AI debate.

        USER REQUEST:
        {user_message}

        CURRENT DEBATE:
        {chr(10).join(debate_history)}

        Your role:
        - improve the proposed solution
        - resolve disagreements
        - make architecture practical
        - optimize implementation

        Current round: {round_num}

        Respond in markdown.
        """

        builder_reply = builder.reply([
            {"role": "user", "content": builder_prompt}
        ])

        debate_history.append(
            f"Builder: {builder_reply}"
        )

        await websocket.send_json({
            "agent": f"🛠 Builder (Round {round_num})",
            "message": builder_reply
        })

        await asyncio.sleep(1)

    # =========================
    # JUDGE
    # =========================

    judge_prompt = f"""
    USER REQUEST:
    {user_message}

    COMPLETE DEBATE:
    {chr(10).join(debate_history)}

    Create a FINAL CONSENSUS.

    Include:
    - final architecture
    - best decisions
    - tradeoffs
    - conclusion

    Respond in markdown.
    """

    judge_reply = judge.reply([
        {"role": "user", "content": judge_prompt}
    ])

    await websocket.send_json({
        "agent": "⚖️ Judge",
        "message": judge_reply
    })