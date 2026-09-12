using System.Security.Cryptography;

namespace FileProcessingToolkit;

public static class FileHasher
{
    public static async Task<string> Sha256Async(string path)
    {
        await using var stream = File.OpenRead(path);
        var hash = await SHA256.HashDataAsync(stream);
        return Convert.ToHexString(hash).ToLowerInvariant();
    }
}
