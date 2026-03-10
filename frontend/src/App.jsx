import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Sparkles, Search, Brain, Lightbulb, FileText, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

function App() {
  const [topic, setTopic] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [output, setOutput] = useState([]); // Log of events
  const [report, setReport] = useState(null);
  const [activeStep, setActiveStep] = useState('idle'); // idle, retrieve, reason, hypothesize, critique, done

  const reportRef = useRef(null);

  const startResearch = async () => {
    if (!topic) return;
    setIsResearching(true);
    setReport(null);
    setOutput([]);
    setActiveStep('retrieve');

    try {
      const response = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) throw new Error('Failed to start research');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '');
            try {
              const data = JSON.parse(dataStr);
              handleEvent(data);
            } catch (e) {
              console.error("Error parsing JSON", e);
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setIsResearching(false);
    }
  };

  const handleEvent = (event) => {
    if (event.status === 'complete') {
      finishResearch();
      return;
    }

    if (event.error) {
      console.error(event.error);
      return;
    }

    // Update active step based on node
    if (event.node) {
      setActiveStep(event.node);

      // Add detailed logs
      let logMessage = '';
      if (event.node === 'retrieve') logMessage = `Reading ${event.data.context?.length || 0} papers...`;
      if (event.node === 'reason') logMessage = `Planning research path...`;
      if (event.node === 'hypothesize') logMessage = `Formulating hypothesis...`;
      if (event.node === 'critique') logMessage = `Reviewer #2 is critiquing...`;

      if (logMessage) {
        setOutput(prev => [...prev, { node: event.node, message: logMessage, details: event.data }]);
      }
    }
  };

  const finishResearch = async () => {
    setIsResearching(false);
    setActiveStep('done');

    // In a real app, we'd reconstruct the state from the events. 
    // Here, we might need to ask the backend for the report if we didn't build it locally.
    // For this demo, let's just construct a simple view or call the report endpoint if we saved state.
    // Since our backend doesn't persist state across requests easily in this "stream" mode without a DB,
    // let's rely on the last "hypothesize" and "critique" data chunks to show something, 
    // OR (better) let's have the backend send the full report as the final event. 
    // But I didn't implement that.

    // Fallback: We can just piece together the last known inputs.
    // Actually, let's just trigger a re-render of the "details" we collected.

    // Wait... the prompt said "implement everything". Let's handle the report data properly.
    // I will extract the final pieces from the `output` log.
  };

  // Helper to extract final report data from logs
  const getFinalReportData = () => {
    const hypothesisData = output.find(o => o.node === 'hypothesize')?.details;
    const critiqueData = output.find(o => o.node === 'critique')?.details;
    const reasonData = output.find(o => o.node === 'reason')?.details;
    const retrieveData = output.find(o => o.node === 'retrieve')?.details;

    if (!hypothesisData) return null;

    return `
# Research Title: ${topic}

## Hypothesis
${hypothesisData.hypothesis}

## Critique
${critiqueData?.feedback || "Pending..."}

## Methodology
${reasonData?.reasoning_trace || "..."}

## Sources
${retrieveData?.context?.join('\n\n') || "..."}
    `;
  };

  const finalReportMarkdown = getFinalReportData();

  return (
    <div className="min-h-screen bg-background relative overflow-hidden flex flex-col items-center py-10 px-4">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-violet-600/20 rounded-full blur-[120px]" />
      </div>

      <div className="z-10 w-full max-w-5xl">
        <header className="mb-12 text-center">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-4"
          >
            <Sparkles size={16} />
            <span>Agentic Research Assistant</span>
          </motion.div>
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 mb-4 tracking-tight">
            Discover the Unknown
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            An autonomous agent that reads, reasons, and hypothesizes novel scientific ideas.
          </p>
        </header>

        <main className="space-y-8">
          {/* Input Section */}
          <section className="glass-card flex gap-4 p-2 items-center">
            <div className="bg-surface/50 p-3 rounded-lg text-slate-400">
              <Search size={20} />
            </div>
            <input
              type="text"
              placeholder="Enter a research topic (e.g., 'CRISPR off-target effects')..."
              className="bg-transparent w-full text-lg text-white outline-none placeholder:text-slate-600"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && startResearch()}
            />
            <button
              onClick={startResearch}
              disabled={isResearching || !topic}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-semibold transition-all flex items-center gap-2"
            >
              {isResearching ? 'Thinking...' : 'Start Research'}
              {!isResearching && <ArrowRight size={18} />}
            </button>
          </section>

          {/* Status Timeline */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatusCard step="retrieve" active={activeStep} icon={FileText} label="Retrieval" />
            <StatusCard step="reason" active={activeStep} icon={Brain} label="Reasoning" />
            <StatusCard step="hypothesize" active={activeStep} icon={Lightbulb} label="Hypothesis" />
            <StatusCard step="critique" active={activeStep} icon={AlertTriangle} label="Critique" />
          </div>

          {/* Live Output Log */}
          <AnimatePresence>
            {output.length > 0 && !finalReportMarkdown && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="glass-card min-h-[200px] max-h-[400px] overflow-y-auto font-mono text-sm space-y-2"
              >
                {output.map((o, i) => (
                  <div key={i} className="flex gap-2 text-slate-300 border-b border-white/5 pb-2">
                    <span className={clsx("font-bold uppercase text-xs w-24 shrink-0 mt-1",
                      o.node === 'retrieve' ? 'text-green-400' :
                        o.node === 'reason' ? 'text-blue-400' :
                          o.node === 'hypothesize' ? 'text-yellow-400' :
                            'text-red-400'
                    )}>[{o.node}]</span>
                    <div>
                      <p>{o.message}</p>
                      {/* Preview of content */}
                      {o.node === 'hypothesize' && (
                        <div className="mt-2 p-3 bg-white/5 rounded text-white/80">
                          {o.details.hypothesis}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Final Report */}
          {finalReportMarkdown && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-card"
            >
              <div className="flex items-center gap-2 mb-6 pb-4 border-b border-white/10">
                <CheckCircle className="text-green-400" />
                <h2 className="text-xl font-semibold">Research Complete. Report Generated.</h2>
              </div>
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown>{finalReportMarkdown}</ReactMarkdown>
              </div>
            </motion.div>
          )}
        </main>
      </div>
    </div>
  );
}

function StatusCard({ step, active, icon: Icon, label }) {
  const stepsOrder = ['idle', 'retrieve', 'reason', 'hypothesize', 'critique', 'done'];
  const isActive = active === step;
  const isPast = stepsOrder.indexOf(active) > stepsOrder.indexOf(step);

  return (
    <div className={clsx(
      "p-4 rounded-xl border transition-all duration-300 flex items-center gap-3",
      isActive ? "bg-blue-500/20 border-blue-500/50 shadow-lg shadow-blue-500/10" :
        isPast ? "bg-surface/30 border-green-500/30 text-green-400" :
          "bg-surface/30 border-white/5 text-slate-500"
    )}>
      <div className={clsx(
        "p-2 rounded-lg",
        isActive ? "bg-blue-500 text-white" :
          isPast ? "bg-green-500/20" : "bg-white/5"
      )}>
        <Icon size={20} />
      </div>
      <span className="font-medium">{label}</span>
      {isActive && (
        <span className="ml-auto w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
      )}
    </div>
  );
}

export default App;
