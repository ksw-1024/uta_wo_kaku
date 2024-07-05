"use client";

import { useState, useRef } from "react";

import { Stage, Layer, Line } from "react-konva";

import IconButton from "@mui/material/IconButton";

import { LuPencil, LuEraser } from "react-icons/lu";

const FreeDrawingComponent = () => {
    const [tool, setTool] = useState("pen");
    const [lines, setLines] = useState<any[]>([]);
    const isDrawing = useRef(false);

    const handleMouseDown = (e: any) => {
        isDrawing.current = true;
        const position = e.target.getStage().getPointerPosition();
        setLines([
            ...lines,
            {
                tool,
                points: [position.x, position.y],
                color: "#df4b26",
                strokeWidth: 0.5,
            },
        ]);
    };

    const handleMouseMove = (e: any) => {
        if (!isDrawing.current) {
            return;
        }
        const position = e.target.getStage().getPointerPosition();
        let lastLine = lines[lines.length - 1];
        lastLine.points = lastLine.points.concat([position.x, position.y]);

        lines.splice(lines.length - 1, 1, lastLine);
        setLines(lines.concat());
    };

    const handleMouseUp = () => {
        isDrawing.current = false;
    };

    const onClickChangeTool = (tool: string) => {
        setTool(tool);
    };

    return (
        <div className="free-drawing-container">
            <Stage
                width={window.innerWidth}
                height={window.innerHeight}
                onMouseDown={handleMouseDown}
                onMousemove={handleMouseMove}
                onMouseUp={handleMouseUp}
            >
                <Layer>
                    {lines.map((line, i) => (
                        <Line
                            key={i}
                            points={line.points}
                            stroke={line.color}
                            strokeWidth={line.strokeWidth}
                            tension={0.5}
                            lineCap="round"
                            lineJoin="round"
                            globalCompositeOperation={
                                line.tool === "eraser" ? "destination-out" : "source-over"
                            }
                        />
                    ))}
                </Layer>
            </Stage>
            <div className="toolbar">
                <IconButton
                    onClick={() => onClickChangeTool("pen")}
                    color={tool === "pen" ? "primary" : "default"}
                >
                    <LuPencil />
                </IconButton>
                <IconButton
                    onClick={() => onClickChangeTool("eraser")}
                    color={tool === "eraser" ? "primary" : "default"}
                >
                    <LuEraser />
                </IconButton>
            </div>
        </div>
    );
};

export default FreeDrawingComponent;

