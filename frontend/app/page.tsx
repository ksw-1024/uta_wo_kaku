import { Input } from "@nextui-org/input";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div>
        <Input label="Enter any text." type="text" />
      </div>
    </section>
  );
}
