# Director agent - orchestrates the writing process

class Director:
    """Director agent that orchestrates the writing process"""
    
    def __init__(self, writer=None, reviewer=None, analyst=None):
        self.name = "Director"
        self.status = "initialized"
        self.writer = writer
        self.reviewer = reviewer
        self.analyst = analyst
    
    def start_writing_process(self):
        """Start the humanized writing process"""
        print(f"{self.name}: Iniciando processo de escrita humanizada...")
        return True
    
    def coordinate_agents(self):
        """Coordinate between different agents"""
        print(f"{self.name}: Coordenando agentes...")
        return True
    
    def coordinate_process(self, content):
        """Coordinate the complete writing process"""
        print(f"{self.name}: Coordenando processo completo...")
        
        # Process with writer
        if self.writer:
            content = self.writer.humanize(content)
        
        # Review with reviewer
        if self.reviewer:
            review_result = self.reviewer.review(content)
            print(f"{self.name}: Revisão concluída. Score: {review_result.get('overall_score', 0):.2f}")
        
        # Analyze with analyst
        if self.analyst:
            insights = self.analyst.analyze(content)
            print(f"{self.name}: Insights obtidos: {insights}")
        
        return content