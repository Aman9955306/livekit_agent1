from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    google
)
import prompts
from tools import lookup_weather, send_slack_message

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=prompts.prompt2,
                         tools=[lookup_weather,send_slack_message]
                         )
    

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        # llm=openai.realtime.RealtimeModel(
        #     voice="coral"
        # )
        llm=google.beta.realtime.RealtimeModel(
        model="gemini-2.0-flash-exp",
        voice="Aoede",
        temperature=0.8,
        instructions="You are a helpful assistant",
    ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="start the conversation with grreetings and ask what brings here today , rpresent salesken dont start asking questions righ way talk like a proffessional sales rep",
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))