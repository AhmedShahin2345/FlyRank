import { Inngest } from "inngest";

export const inngest = new Inngest({
  id: "flyrank-decision-flow",
  name: "FlyRank AI Decision Flow",
  eventKey: process.env.INNGEST_EVENT_KEY,
  signingKey: process.env.INNGEST_SIGNING_KEY,
});