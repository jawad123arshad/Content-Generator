# # """
# # Enhanced text processing utilities
# # """

# # import re
# # from typing import List, Tuple

# # class TextProcessor:
# #     """Text processing utilities with improved prompt engineering"""
    
# #     def enhance_prompt(self, prompt: str, max_words: int, num_lines: int) -> str:
# #         """Enhance prompt with better instructions for the model"""
        
# #         # Clean the prompt
# #         prompt = prompt.strip()
        
# #         # Create a structured prompt based on content type detection
# #         content_type = self._detect_content_type(prompt)
        
# #         # Base instruction
# #         enhanced = f"Generate {self._get_content_type_description(content_type)}.\n\n"
        
# #         # Add specific instructions based on content type
# #         if content_type == "product_description":
# #             enhanced += "Write a compelling product description that includes:\n"
# #             enhanced += "- Key features and benefits\n"
# #             enhanced += "- Target audience\n"
# #             enhanced += "- What makes it unique\n"
# #             enhanced += "- Call to action\n\n"
# #         elif content_type == "story":
# #             enhanced += "Write a short story with:\n"
# #             enhanced += "- Engaging opening\n"
# #             enhanced += "- Clear beginning, middle, end\n"
# #             enhanced += "- Descriptive language\n\n"
# #         elif content_type == "email":
# #             enhanced += "Write a professional email that includes:\n"
# #             enhanced += "- Clear subject line\n"
# #             enhanced += "- Proper greeting\n"
# #             enhanced += "- Main message\n"
# #             enhanced += "- Professional closing\n\n"
# #         elif content_type == "social_media":
# #             enhanced += "Write an engaging social media post that:\n"
# #             enhanced += "- Grabs attention\n"
# #             enhanced += "- Includes relevant hashtags\n"
# #             enhanced += "- Encourages engagement\n\n"
        
# #         # Add word and line constraints
# #         enhanced += f"Topic: {prompt}\n\n"
# #         enhanced += f"Requirements:\n"
# #         enhanced += f"- Write {num_lines} paragraph(s)\n"
# #         enhanced += f"- Each paragraph should be approximately {max_words} words\n"
# #         enhanced += f"- Make it engaging and well-structured\n"
# #         enhanced += f"- Start directly with the content, no meta-commentary\n\n"
# #         enhanced += "Content:\n"
        
# #         return enhanced
    
# #     def _detect_content_type(self, prompt: str) -> str:
# #         """Detect the type of content to generate"""
# #         prompt_lower = prompt.lower()
        
# #         content_patterns = {
# #             "product_description": ["product", "description", "item", "device", "gadget", "laptop", "phone"],
# #             "story": ["story", "tale", "narrative", "fiction"],
# #             "email": ["email", "mail", "message"],
# #             "social_media": ["post", "tweet", "social", "instagram", "facebook"],
# #             "article": ["article", "blog", "post", "write-up"],
# #             "review": ["review", "feedback", "opinion"],
# #             "advertisement": ["ad", "advertisement", "promote", "marketing"]
# #         }
        
# #         for content_type, keywords in content_patterns.items():
# #             if any(keyword in prompt_lower for keyword in keywords):
# #                 return content_type
        
# #         return "general"
    
# #     def _get_content_type_description(self, content_type: str) -> str:
# #         """Get human-readable description of content type"""
# #         descriptions = {
# #             "product_description": "a detailed and persuasive product description",
# #             "story": "an engaging short story",
# #             "email": "a professional email",
# #             "social_media": "an engaging social media post",
# #             "article": "an informative article",
# #             "review": "a helpful review",
# #             "advertisement": "a compelling advertisement",
# #             "general": "high-quality content"
# #         }
# #         return descriptions.get(content_type, "high-quality content")
    
# #     def post_process(self, generated_text: str, original_prompt: str, 
# #                     max_words: int, num_lines: int) -> str:
# #         """Clean and format generated text"""
        
# #         # Remove the original prompt and instructions if they appear
# #         lines = generated_text.split('\n')
# #         cleaned_lines = []
        
# #         for line in lines:
# #             line = line.strip()
# #             # Skip instruction lines and meta-commentary
# #             if (line and 
# #                 not line.startswith('Generate') and 
# #                 not line.startswith('Topic:') and 
# #                 not line.startswith('Requirements:') and
# #                 not line.startswith('Content:') and
# #                 not line.startswith('I'd like to') and
# #                 not 'disclaimer' not in line.lower()):
# #                 cleaned_lines.append(line)
        
# #         cleaned_text = ' '.join(cleaned_lines)
        
# #         # Remove any remaining meta-commentary
# #         cleaned_text = re.sub(r'\([^)]*\)', '', cleaned_text)  # Remove parentheticals
# #         cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)  # Remove brackets
        
# #         # Clean up extra spaces
# #         cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
# #         # Split into paragraphs
# #         if num_lines > 1:
# #             return self._split_into_paragraphs(cleaned_text, num_lines)
        
# #         # Truncate to word limit
# #         return self._truncate_to_words(cleaned_text, max_words)
    
# #     def _split_into_paragraphs(self, text: str, num_paragraphs: int) -> str:
# #         """Split text into approximately equal paragraphs"""
# #         sentences = re.split(r'(?<=[.!?])\s+', text)
        
# #         if len(sentences) <= num_paragraphs:
# #             return '\n\n'.join(sentences)
        
# #         # Distribute sentences into paragraphs
# #         sentences_per_para = len(sentences) // num_paragraphs
# #         paragraphs = []
        
# #         for i in range(num_paragraphs):
# #             start = i * sentences_per_para
# #             end = start + sentences_per_para if i < num_paragraphs - 1 else len(sentences)
# #             paragraph = ' '.join(sentences[start:end])
# #             paragraphs.append(paragraph)
        
# #         return '\n\n'.join(paragraphs)
    
# #     def _truncate_to_words(self, text: str, max_words: int) -> str:
# #         """Truncate text to approximate word count"""
# #         words = text.split()
# #         if len(words) > max_words:
# #             words = words[:max_words]
# #             return ' '.join(words) + '...'
# #         return text



# """
# Enhanced text processing utilities
# """

# import re


# class TextProcessor:
#     """Text processing utilities with improved prompt engineering"""

#     def enhance_prompt(self, prompt: str, max_words: int, num_lines: int) -> str:
#         """Enhance prompt with better instructions for the model"""

#         prompt = prompt.strip()
#         content_type = self._detect_content_type(prompt)

#         enhanced = f"Generate {self._get_content_type_description(content_type)}.\n\n"

#         if content_type == "product_description":
#             enhanced += (
#                 "Write a compelling product description that includes:\n"
#                 "- Key features and benefits\n"
#                 "- Target audience\n"
#                 "- What makes it unique\n"
#                 "- Call to action\n\n"
#             )

#         elif content_type == "story":
#             enhanced += (
#                 "Write a short story with:\n"
#                 "- Engaging opening\n"
#                 "- Clear beginning, middle, end\n"
#                 "- Descriptive language\n\n"
#             )

#         elif content_type == "email":
#             enhanced += (
#                 "Write a professional email that includes:\n"
#                 "- Clear subject line\n"
#                 "- Proper greeting\n"
#                 "- Main message\n"
#                 "- Professional closing\n\n"
#             )

#         elif content_type == "social_media":
#             enhanced += (
#                 "Write an engaging social media post that:\n"
#                 "- Grabs attention\n"
#                 "- Includes relevant hashtags\n"
#                 "- Encourages engagement\n\n"
#             )

#         enhanced += (
#             f"Topic: {prompt}\n\n"
#             f"Requirements:\n"
#             f"- Write {num_lines} paragraph(s)\n"
#             f"- Each paragraph should be approximately {max_words} words\n"
#             f"- Make it engaging and well-structured\n"
#             f"- Start directly with the content, no meta-commentary\n\n"
#             "Content:\n"
#         )

#         return enhanced

#     def _detect_content_type(self, prompt: str) -> str:
#         prompt_lower = prompt.lower()

#         content_patterns = {
#             "product_description": ["product", "description", "item", "device", "gadget", "laptop", "phone"],
#             "story": ["story", "tale", "narrative", "fiction"],
#             "email": ["email", "mail", "message"],
#             "social_media": ["post", "tweet", "social", "instagram", "facebook"],
#             "article": ["article", "blog", "write-up"],
#             "review": ["review", "feedback", "opinion"],
#             "advertisement": ["ad", "advertisement", "promote", "marketing"],
#         }

#         for content_type, keywords in content_patterns.items():
#             if any(keyword in prompt_lower for keyword in keywords):
#                 return content_type

#         return "general"

#     def _get_content_type_description(self, content_type: str) -> str:
#         descriptions = {
#             "product_description": "a detailed and persuasive product description",
#             "story": "an engaging short story",
#             "email": "a professional email",
#             "social_media": "an engaging social media post",
#             "article": "an informative article",
#             "review": "a helpful review",
#             "advertisement": "a compelling advertisement",
#             "general": "high-quality content",
#         }
#         return descriptions.get(content_type, "high-quality content")

#     def post_process(
#         self,
#         generated_text: str,
#         original_prompt: str,
#         max_words: int,
#         num_lines: int,
#     ) -> str:
#         """Clean and format generated text"""

#         lines = generated_text.split("\n")
#         cleaned_lines = []

#         for line in lines:
#             line = line.strip()

#             if (
#                 line
#                 and not line.startswith("Generate")
#                 and not line.startswith("Topic:")
#                 and not line.startswith("Requirements:")
#                 and not line.startswith("Content:")
#                 and not line.startswith("I'd like to")
#                 and "disclaimer" not in line.lower()
#             ):
#                 cleaned_lines.append(line)

#         cleaned_text = " ".join(cleaned_lines)

#         cleaned_text = re.sub(r"\([^)]*\)", "", cleaned_text)
#         cleaned_text = re.sub(r"\[[^\]]*\]", "", cleaned_text)
#         cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

#         if num_lines > 1:
#             return self._split_into_paragraphs(cleaned_text, num_lines)

#         return self._truncate_to_words(cleaned_text, max_words)

#     def _split_into_paragraphs(self, text: str, num_paragraphs: int) -> str:
#         sentences = re.split(r"(?<=[.!?])\s+", text)

#         if len(sentences) <= num_paragraphs:
#             return "\n\n".join(sentences)

#         sentences_per_para = len(sentences) // num_paragraphs
#         paragraphs = []

#         for i in range(num_paragraphs):
#             start = i * sentences_per_para
#             end = (
#                 start + sentences_per_para
#                 if i < num_paragraphs - 1
#                 else len(sentences)
#             )
#             paragraphs.append(" ".join(sentences[start:end]))

#         return "\n\n".join(paragraphs)

#     def _truncate_to_words(self, text: str, max_words: int) -> str:
#         words = text.split()

#         if len(words) > max_words:
#             return " ".join(words[:max_words]) + "..."

#         return text

"""
Fixed text processing utilities - NO ECHOING of instructions
"""

import re
from typing import List

class TextProcessor:
    """Text processing utilities - fixed to prevent instruction echoing"""
    
    def enhance_prompt(self, prompt: str, max_words: int, num_lines: int) -> str:
        """Create a prompt that won't be echoed back"""
        
        # Clean the prompt
        prompt = prompt.strip()
        
        # Different approach - use examples instead of instructions
        examples = {
            "laptop": "The latest XPS 15 combines powerful performance with elegant design. Featuring a 12th Gen Intel Core i7 processor and 16GB of RAM, it handles demanding tasks with ease. The 4K OLED display brings visuals to life with stunning clarity and color accuracy.",
            
            "phone": "Experience photography like never before with the ProCamera 15. Its triple-lens system captures professional-quality photos in any lighting condition. The all-day battery life keeps you connected from morning to night.",
            
            "default": "This premium product delivers exceptional quality and performance. Crafted with attention to detail, it exceeds expectations in every way. Users appreciate its reliability and innovative features."
        }
        
        # Detect content type
        content_type = "default"
        prompt_lower = prompt.lower()
        if "laptop" in prompt_lower:
            content_type = "laptop"
        elif "phone" in prompt_lower or "smartphone" in prompt_lower:
            content_type = "phone"
        
        # Use a simple prompt structure that won't be echoed
        if num_lines > 1:
            enhanced = f"Write a {num_lines}-paragraph product description for: {prompt}\n\n"
        else:
            enhanced = f"Write a product description for: {prompt}\n\n"
        
        # Add a very brief example (but not in a way that gets echoed)
        enhanced += f"Example: {examples[content_type]}\n\n"
        enhanced += "Now write a new description:\n"
        
        return enhanced
    
    def post_process(self, generated_text: str, original_prompt: str, 
                    max_words: int, num_lines: int) -> str:
        """Clean up generated text"""
        
        # Split into lines
        lines = generated_text.split('\n')
        
        # Filter out instruction lines and meta-commentary
        filtered_lines = []
        for line in lines:
            line = line.strip()
            
            # Skip lines that look like instructions
            if (line and 
                not line.startswith('Write') and
                not line.startswith('Example') and
                not line.startswith('Now write') and
                not line.startswith('Topic:') and
                not line.startswith('Generate') and
                not 'paragraph' not in line.lower() and
                not line.startswith('-') and
                len(line) > 10):  # Skip very short lines
                filtered_lines.append(line)
        
        # If we filtered out too much, use original but clean it
        if len(filtered_lines) < 2:
            # Take the last part of the generation (after instructions)
            text = generated_text
            if 'Now write a new description:' in text:
                text = text.split('Now write a new description:')[-1]
            elif 'Example:' in text:
                parts = text.split('Example:')
                if len(parts) > 1:
                    text = parts[-1]
            
            # Clean up
            lines = text.split('\n')
            filtered_lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 20]
        
        # Join and clean
        result = ' '.join(filtered_lines)
        
        # Remove any remaining instruction-like text
        result = re.sub(r'Write a \d+-paragraph.*?:', '', result)
        result = re.sub(r'Example:.*?\.', '', result)
        
        # Clean up spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Split into paragraphs if needed
        if num_lines > 1 and len(result) > 100:
            return self._split_into_paragraphs(result, num_lines)
        
        # Truncate to word limit
        return self._truncate_to_words(result, max_words)
    
    def _split_into_paragraphs(self, text: str, num_paragraphs: int) -> str:
        """Split text into paragraphs"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) <= num_paragraphs:
            return '\n\n'.join(sentences)
        
        # Distribute sentences
        sentences_per_para = len(sentences) // num_paragraphs
        paragraphs = []
        
        for i in range(num_paragraphs):
            start = i * sentences_per_para
            end = start + sentences_per_para if i < num_paragraphs - 1 else len(sentences)
            paragraph = ' '.join(sentences[start:end])
            paragraphs.append(paragraph)
        
        return '\n\n'.join(paragraphs)
    
    def _truncate_to_words(self, text: str, max_words: int) -> str:
        """Truncate to word count"""
        words = text.split()
        if len(words) > max_words:
            words = words[:max_words]
            return ' '.join(words) + '...'
        return text