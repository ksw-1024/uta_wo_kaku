"use client";

import { Brush } from "lucide-react";
import { Button, Link } from "@nextui-org/react";

import { ThemeImage } from "@/components/theme-image";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <ThemeImage
        alt="Logo"
        srcLight="/logo-black.svg"
        srcDark="/logo-white.svg"
        width={1000}
        height={100}
      />
      <div>
        <Button size="lg" href="/create" as={Link} endContent={<Brush size={16} />}>つくる</Button>
      </div>
      <Link href={"http://localhost:8888"}>再生ページ</Link>
    </section>
  );
}
