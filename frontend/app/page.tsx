"use client";

import { useState } from "react";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/react";

import BPMtimer from "@/components/BPMtimer";

export default function Home() {
  const [text, setText] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/render_voice", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: text,
        }),
      });
      const jsonData = await response.json();

      alert("テキストを送信しました");
    } catch (err) {
      alert("テキストの送信に失敗しました")
    }
  }

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div>
        <form onSubmit={handleSubmit}>
          <Input
            required
            label="Text"
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <Button type="submit">送信</Button>
        </form>
        <Button>TEST</Button>
        <BPMtimer></BPMtimer>
      </div>
    </section>
  );
}
