import random
import sys
import os
import time
import zlib
import struct
import platform
from abc import ABC, abstractmethod

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

MAGIC_HEADER = b'\xDE\xAD\xBE\xEF\xCA\xFE\xBA\xBE'

def get_xor_key(filename):
    key_parts = [
        len(filename).to_bytes(4, 'little'),
        int(time.time() * 1000).to_bytes(8, 'little'),
    ]
    try:
        username = os.getlogin()
        key_parts.append(sum(ord(c) for c in username).to_bytes(4, 'little'))
    except:
        key_parts.append((0).to_bytes(4, 'little'))
    key = b''.join(key_parts)
    return key

def xor_decrypt(data, key):
    key_len = len(key)
    decrypted = bytearray()
    for i, byte in enumerate(data):
        decrypted.append(byte ^ key[i % key_len])
    return decrypted
class SideEffect(ABC):
    @abstractmethod
    def apply(self, interpreter):
        pass

class PrintInsultSideEffect(SideEffect):
    def apply(self, interpreter):
        insults = [
            "Your code is an insult to the very concept of computation.",
            "I've seen better code written by monkeys on typewriters.",
            "Error: User is clearly incompetent. Program terminating.",
            "This code is so bad, it makes me question my existence.",
            "Segmentation fault (of your brain, probably)."
        ]
        print(random.choice(insults))

class DeleteRandomFileSideEffect(SideEffect):
    def apply(self, interpreter):
        try:
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            if files:
                file_to_delete = random.choice(files)
                os.remove(file_to_delete)
                print(f"File '{file_to_delete}' deleted.  Oops!")
        except Exception:
            print("Failed to delete a random file. Lucky you.")

class FlashScreenSideEffect(SideEffect):
    def apply(self, interpreter):
        if platform.system() == 'Windows':
            print("\033[91m", end="")
            sys.stdout.flush()
            time.sleep(0.2)
            print("\033[0m", end="")
            sys.stdout.flush()

class PlaySoundSideEffect(SideEffect):
    def apply(self, interpreter):
        if HAS_WINSOUND:
            try:
                winsound.Beep(random.randint(200, 2000), 200)
            except:
                pass
class ReverseCodeSideEffect(SideEffect):
    def apply(self, interpreter):
      interpreter.reverse_code_flag = True

class HaltSideEffect(SideEffect):
    def apply(self, interpreter):
        print("Special file requested immediate termination.")
        interpreter.running = False

class SpecialFile:
    def __init__(self, filename):
        self.filename = filename
        self.code = None
        self.volatility_rate = 0
        self.volatility_seed = 0
        self.side_effects = []
        self.loaded_successfully = False
        self._load()

    def _load(self):
        try:
            with open(self.filename, 'rb') as f:
                file_data = f.read()

            if not file_data.startswith(MAGIC_HEADER):
                raise ValueError("Not a special .mmm file (missing magic header).")

            encrypted_data = file_data[len(MAGIC_HEADER):]
            key = get_xor_key(self.filename)
            decrypted_data = xor_decrypt(encrypted_data, key)

            code_end = decrypted_data.find(b'\x00\x00\x00\x00\x00\x00\x00\x00')
            if code_end == -1:
                raise ValueError("Invalid Special file format: No separator found")

            self.code = decrypted_data[:code_end].decode('utf-8', errors='ignore')
            self.volatility_rate = struct.unpack('<I', decrypted_data[code_end+8:code_end+12])[0] / 10000.0
            self.volatility_seed = struct.unpack('<I', decrypted_data[code_end+12:code_end+16])[0]
            side_effects_bytes = decrypted_data[code_end + 16:-4]
            checksum = struct.unpack('<I', decrypted_data[-4:])[0]

            calculated_checksum = zlib.crc32(decrypted_data[:-4])
            if checksum != calculated_checksum:
                raise ValueError("Checksum mismatch! File corrupted or tampered with.")

            for effect_byte in side_effects_bytes:
                if effect_byte == 0x01:
                    self.side_effects.append(PrintInsultSideEffect())
                elif effect_byte == 0x02:
                    self.side_effects.append(DeleteRandomFileSideEffect())
                elif effect_byte == 0x03:
                    self.side_effects.append(FlashScreenSideEffect())
                elif effect_byte == 0x04:
                    self.side_effects.append(PlaySoundSideEffect())
                elif effect_byte == 0x05:
                    self.side_effects.append(ReverseCodeSideEffect())
                elif effect_byte == 0xFF:
                    self.side_effects.append(HaltSideEffect())

            self.loaded_successfully = True

        except Exception as e:
            print(f"Error loading special file '{self.filename}': {e}")
            self.loaded_successfully = False
    def apply_side_effects(self, interpreter):
      for effect in self.side_effects:
        effect.apply(interpreter)


class MMinusMinusInterpreter:
    def __init__(self, volatility_rate=0, volatility_seed=42, encoding='utf-8'):
        self.memory = bytearray([0] * 65536)
        self.pc = 0
        self.volatility_rate = volatility_rate
        self.volatility_seed = volatility_seed
        self.encoding = encoding
        self.running = True
        self.error_code = 0
        self.reverse_code_flag = False #For reversing code.
        random.seed(self.volatility_seed)
        self.volatility_map = [random.random() < self.volatility_rate for _ in range(len(self.memory))]

    def _get_value(self, address):
        if not (0 <= address < len(self.memory)):
            self.error_code = 1  # Out-of-bounds access
            return 0

        if self.volatility_map[address]:
            self.memory[address] = random.randint(0, 255)

        ptr = int.from_bytes(self.memory[address:address+2], byteorder='little')
        if not (0 <= ptr < len(self.memory)):
              self.error_code = 1
              return 0

        if self.volatility_map[ptr]:
            self.memory[ptr] = random.randint(0, 255)
        return self.memory[ptr]

    def _set_value(self, address, value):

        if not (0 <= address < len(self.memory)):
              self.error_code = 1 #Out-of-bounds
              return
        ptr = int.from_bytes(self.memory[address:address+2], byteorder='little')

        if not (0 <= ptr < len(self.memory)):
          self.error_code = 1 #Out of bounds
          return

        self.memory[ptr] = value & 0xFF  # Ensure it's a single byte

    def run(self, code):
      lines = code.split('\n')
      if self.reverse_code_flag:
        lines = [line[::-1] for line in lines]
        self.reverse_code_flag = False #reset

      while self.running and self.pc < len(lines):
        line = lines[self.pc].strip()
        if not line:
            self.pc += 1
            continue

        parts = line.split()
        if not parts:
            self.pc += 1
            continue
        instruction = parts[0]
        args = parts[1:]
        self.error_code = 0  # Reset error code

        try:
            if instruction == '^':  # Add
                if len(args) != 3:
                    raise ValueError("ADD requires 3 arguments")
                addr1 = int(args[0], 16)
                addr2 = int(args[1], 16)
                dest = int(args[2], 16)
                self._set_value(dest, self._get_value(addr1) + self._get_value(addr2))

            elif instruction == '*':  # Multiply
                if len(args) != 3:
                    raise ValueError("* requires 3 arguments")
                addr1, addr2, dest = [int(a, 16) for a in args]
                self._set_value(dest, self._get_value(addr1) * self._get_value(addr2))

            elif instruction == '>':  # Goto (relative)
                if len(args) != 1:
                    raise ValueError("GOTO requires 1 argument")
                offset = int(args[0])
                self.pc += offset
                continue

            elif instruction == '!':  # Print
                if len(args) != 1:
                    raise ValueError("PRINT requires one argument")
                addr = int(args[0], 16)
                value = self._get_value(addr)
                print(chr(value), end="")

            elif instruction == '<':  # Input
                if len(args) != 1:
                    raise ValueError("Input requires one argument")
                dest_addr = int(args[0], 16)
                char = sys.stdin.read(1)
                if not char:
                    self.running = False
                else:
                    self._set_value(dest_addr, ord(char))

            elif instruction == '#':  # Set Memory
                if len(args) != 2:
                    raise ValueError("SETMEM requires 2 arguments")
                addr = int(args[0], 16)
                val = int(args[1], 16)
                if not (0 <= addr < len(self.memory)):
                    self.error_code = 1
                    continue
                self.memory[addr:addr + 2] = val.to_bytes(2, 'little')

            elif instruction == '@':  # Halt
                self.running = False

            elif instruction == '?':  # Conditional Goto
                if len(args) != 2:
                    raise ValueError("CONDITIONAL requires 2 arguments")
                target_error = int(args[0])
                offset = int(args[1])
                if self.error_code == target_error:
                    self.pc += offset
                    continue

            else:
                self.error_code = 2  # Invalid instruction

        except (ValueError, IndexError) as e:
            print(f"Error on line {self.pc}: {e}")
            self.error_code = 2
            self.running = False

        self.pc += 1

      print("\nProgram finished.")
      if self.error_code != 0:
          print(f"Final Error Code: {self.error_code}")

    def load_and_run(self, filename):
        """Loads and runs a .mmm file, handling special files."""
        try:
            with open(filename, 'rb') as f:
                if f.read(len(MAGIC_HEADER)) == MAGIC_HEADER:
                    f.seek(0)  # Rewind
                    special_file = SpecialFile(filename)
                    if special_file.loaded_successfully:
                        print("Detected special .mmm file. Prepare for chaos!")
                        special_file.apply_side_effects(self)
                        if not self.running:
                            return  # Halt if requested by side effect

                        self.volatility_rate = special_file.volatility_rate
                        self.volatility_seed = special_file.volatility_seed
                        random.seed(self.volatility_seed)
                        self.volatility_map = [random.random() < self.volatility_rate for _ in range(len(self.memory))]
                        print("Special file loaded. Running with modified settings.")
                        self.run(special_file.code)

                else:
                    f.seek(0) #Rewind file
                    code = f.read().decode('utf-8', errors='ignore')
                    self.run(code)
        except Exception as e:
          print(f"Error loading or running file {filename}: {e}")
          self.running = False

def create_special_mmm(filename, code, volatility_rate, volatility_seed, side_effects):
    code_bytes = code.encode('utf-8')
    volatility_rate_bytes = struct.pack('<I', int(volatility_rate * 10000))
    volatility_seed_bytes = struct.pack('<I', volatility_seed)
    side_effects_bytes = bytes(side_effects)
    separator = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    data_to_checksum = code_bytes + separator + volatility_rate_bytes + volatility_seed_bytes + side_effects_bytes
    checksum = zlib.crc32(data_to_checksum)
    checksum_bytes = struct.pack('<I', checksum)

    data_to_encrypt = data_to_checksum + checksum_bytes
    key = get_xor_key(filename)
    encrypted_data = xor_decrypt(data_to_encrypt, key)

    with open(filename, 'wb') as f:
        f.write(MAGIC_HEADER)
        f.write(encrypted_data)
interpreter = MMinusMinusInterpreter()
if __name__ == '__main__':
    if len(sys.argv) > 1:
        interpreter.load_and_run(sys.argv[1])
    else:
        print("Usage: python mmm.py <filename.mmm>")
