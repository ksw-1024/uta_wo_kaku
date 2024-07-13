"use client";

import { useState } from "react";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/react";
import Link from "next/link";


export default function Home() {
    const [text, setText] = useState("");
    const [count, setCount] = useState("");

    const handleSubmit_build = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8888/render_voice", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: text,
                }),
            });
            const jsonData = await response.json();

            if (jsonData["fileUrl"] == "TOO MANY LETTERS") {
                alert("文字数が多すぎます。8発音までにおさめてください。")
                return
            }
            alert("テキストを送信しました");
        } catch (err) {
            alert("テキストの送信に失敗しました");
        }
    };

    const handleSubmit_glue = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8888/glue", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
            });
            const jsonData = await response.json();

            console.log(jsonData);

            alert("くっつけに成功しました");
        } catch (err) {
            alert("くっつけに失敗しました");
        }
    };

    const handleSubmit_auto = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8888/auto_onomatope", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    count: Number(count),
                }),
            });
            const jsonData = await response.json();

            alert("成功しました");
        } catch (err) {
            alert("失敗しました");
        }
    };

    return (
        <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
            <div>
                <form onSubmit={handleSubmit_build}>
                    <Input
                        required
                        label="Text"
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                    <Button type="submit">送信</Button>
                </form>
            </div>
            <div className="mt-5">
                <form onSubmit={handleSubmit_glue}>
                    <Button type="submit">くっつける</Button>
                </form>
            </div>
            <div className="mt-5">
                <form onSubmit={handleSubmit_auto}>
                    <Input
                        required
                        label="回数"
                        type="number"
                        value={count}
                        onChange={(e) => setCount(e.target.value)}
                    />
                    <Button type="submit">送信</Button>
                </form>
            </div>
            <Link href={"http://localhost:8888"}>再生ページ</Link>
        </section>
    );
}
